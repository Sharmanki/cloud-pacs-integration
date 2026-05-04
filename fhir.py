import json
import requests
from hl7apy.core import Message

raw_hl7 = (
    "MSH|^~\\&|HIS|TORONTO_GEN|FHIR|TEST|20240415||ADT^A01|MSG001|P|2.5\r"
    "PID|1||12345^^^MRN||KUMAR^ANKIT^^||19900315|M|||123 Main St^^Toronto^ON^M5V1A1^CA\r"
    "PV1|1|I|RAD^101^A|||Dr.Smith|||RAD"
)

msg = Message("ADT_A01", version="2.5")
msg.msh.msh_9 = "ADT^A01"

segments = raw_hl7.strip().split("\r")
pid = None
for seg in segments:
    if seg.startswith("PID"):
        pid = seg.split("|")
        break

patient_id  = pid[3].split("^")[0]
family_name = pid[5].split("^")[0]
given_name  = pid[5].split("^")[1]
dob_raw     = pid[7]
gender_raw  = pid[8]

dob = f"{dob_raw[0:4]}-{dob_raw[4:6]}-{dob_raw[6:8]}"
gender = "male" if gender_raw == "M" else "female"

fhir_patient = {
    "resourceType": "Patient",
    "identifier": [{
        "system": "urn:oid:mrn",
        "value": patient_id
    }],
    "name": [{
        "family": family_name,
        "given": [given_name]
    }],
    "birthDate": dob,
    "gender": gender
}

print("=" * 50)
print("FHIR Patient Resource Built:")
print("=" * 50)
print(json.dumps(fhir_patient, indent=2))

print("\nPosting to HAPI FHIR public server...")

response = requests.post(
    "https://hapi.fhir.org/baseR4/Patient",
    headers={"Content-Type": "application/fhir+json"},
    json=fhir_patient
)

print(f"\nServer Response: {response.status_code}")
print(json.dumps(response.json(), indent=2))