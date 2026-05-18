# api.py
# HL7 → FHIR REST API Microservice
# POST an HL7 message → get FHIR Patient JSON back

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import logging

# ------------------------------------------------
# LOGGING SETUP
# ------------------------------------------------
logging.getLogger("pika").setLevel(logging.WARNING)
logging.basicConfig(
    filename="api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)

# ------------------------------------------------
# FASTAPI APP
# ------------------------------------------------
app = FastAPI(
    title="HL7 to FHIR Integration API",
    description="Accepts raw HL7 v2 messages and transforms them to FHIR R4 resources",
    version="1.0.0"
)

# ------------------------------------------------
# REQUEST MODEL — what the API accepts
# ------------------------------------------------
class HL7Message(BaseModel):
    message: str

# ------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------
def parse_pid(pid_segment):
    try:
        fields      = pid_segment.split("|")
        mrn         = fields[3].split("^")[0]
        family_name = fields[5].split("^")[0]
        given_name  = fields[5].split("^")[1]
        dob_raw     = fields[7]
        gender_raw  = fields[8]
        dob         = dob_raw[0:4] + "-" + dob_raw[4:6] + "-" + dob_raw[6:8]
        gender      = "male" if gender_raw == "M" else "female"
        return {
            "mrn":       mrn,
            "family":    family_name,
            "given":     given_name,
            "birthDate": dob,
            "gender":    gender
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse PID segment: {e}")

def build_fhir_patient(patient):
    return {
        "resourceType": "Patient",
        "name": [{
            "family": patient["family"],
            "given":  [patient["given"]]
        }],
        "birthDate": patient["birthDate"],
        "gender":    patient["gender"]
    }

# ------------------------------------------------
# ROUTES
# ------------------------------------------------

# Route 1 — Health check
@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "HL7 to FHIR Integration API",
        "version": "1.0.0"
    }

# Route 2 — Transform HL7 to FHIR (without posting to server)
@app.post("/transform")
def transform_hl7(body: HL7Message):
    logging.info("Transform request received")

    # Find PID segment
    segments = body.message.strip().split("\r")
    pid_seg = None
    for seg in segments:
        if seg.startswith("PID"):
            pid_seg = seg
            break

    if not pid_seg:
        raise HTTPException(status_code=400, detail="No PID segment found in HL7 message")

    # Parse and build FHIR
    patient = parse_pid(pid_seg)
    fhir_patient = build_fhir_patient(patient)

    logging.info(f"Transformed: {patient['given']} {patient['family']} | {patient['gender']}")

    return {
        "status": "success",
        "patient": patient,
        "fhir_resource": fhir_patient
    }

# Route 3 — Transform AND post to FHIR server
@app.post("/transform-and-post")
def transform_and_post(body: HL7Message):
    logging.info("Transform and post request received")

    # Find PID segment
    segments = body.message.strip().split("\r")
    pid_seg = None
    for seg in segments:
        if seg.startswith("PID"):
            pid_seg = seg
            break

    if not pid_seg:
        raise HTTPException(status_code=400, detail="No PID segment found in HL7 message")

    # Parse and build FHIR
    patient = parse_pid(pid_seg)
    fhir_patient = build_fhir_patient(patient)

    # Post to FHIR server
    try:
        response = requests.post(
            "https://hapi.fhir.org/baseR4/Patient",
            headers={
                "Content-Type": "application/fhir+json",
                "Prefer": "return=representation"
            },
            json=fhir_patient,
            timeout=10
        )

        if response.status_code == 201:
            fhir_id = response.json().get("id", "unknown")
            logging.info(f"SUCCESS: {patient['mrn']} | FHIR ID={fhir_id}")
            return {
                "status":        "success",
                "fhir_id":       fhir_id,
                "patient":       patient,
                "fhir_resource": fhir_patient
            }
        else:
            logging.error(f"FHIR server error: {response.status_code}")
            raise HTTPException(
                status_code=502,
                detail=f"FHIR server returned: {response.status_code}"
            )

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="FHIR server timeout")

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Cannot connect to FHIR server")

# Route 4 — Get API stats
@app.get("/stats")
def get_stats():
    return {
        "service":     "HL7 to FHIR Integration API",
        "endpoints": [
            "GET  /          — health check",
            "POST /transform — transform HL7 to FHIR only",
            "POST /transform-and-post — transform + post to FHIR server",
            "GET  /stats     — this endpoint"
        ],
        "fhir_server": "https://hapi.fhir.org/baseR4"
    }