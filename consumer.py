# consumer.py
# HL7 → FHIR Integration Engine
# Production-grade: logging, error handling, counters, clean shutdown

import pika
import requests
import logging

# ------------------------------------------------
# SUPPRESS pika debug messages
# ------------------------------------------------
logging.getLogger("pika").setLevel(logging.WARNING)

# ------------------------------------------------
# LOGGING SETUP — audit trail for every message
# ------------------------------------------------
logging.basicConfig(
    filename="hl7_processing.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Print logs to console at the same time
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

# ------------------------------------------------
# COUNTERS — track session statistics
# ------------------------------------------------
processed_count = 0
failed_count = 0

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
        logging.error(f"Failed to parse PID segment: {e}")
        return None

def build_fhir_patient(patient):
    # No identifier — server assigns fresh ID every time
    # Avoids 412 Precondition Failed on HAPI public server
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
# MAIN CALLBACK — called for every message
# ------------------------------------------------
def process_hl7_message(ch, method, properties, body):
    global processed_count, failed_count

    print("\n" + "="*50)
    logging.info("New message received from queue")

    try:
        # Decode bytes to string
        raw_hl7 = body.decode()

        # Find PID segment
        segments = raw_hl7.strip().split("\r")
        pid_seg = None
        for seg in segments:
            if seg.startswith("PID"):
                pid_seg = seg
                break

        if not pid_seg:
            logging.warning("No PID segment found — skipping message")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        # Parse patient
        patient = parse_pid(pid_seg)
        if not patient:
            logging.error("Failed to parse patient — skipping")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            failed_count += 1
            return

        logging.info(f"Parsed: MRN={patient['mrn']} | {patient['given']} {patient['family']} | {patient['gender']} | DOB={patient['birthDate']}")

        # Build FHIR resource
        fhir_patient = build_fhir_patient(patient)

        # Post to FHIR server
        response = requests.post(
            "https://hapi.fhir.org/baseR4/Patient",
            headers={
                "Content-Type": "application/fhir+json",
                "Prefer": "return=representation"
            },
            json=fhir_patient,
            timeout=10
        )

        # Handle response
        if response.status_code == 201:
            fhir_id = response.json().get("id", "unknown")
            processed_count += 1
            logging.info(f"SUCCESS: MRN={patient['mrn']} | FHIR ID={fhir_id} | Status=201")
            logging.info(f"Session stats: Processed={processed_count} | Failed={failed_count}")
        else:
            failed_count += 1
            logging.error(f"FHIR server error: MRN={patient['mrn']} | Status={response.status_code}")

        # Acknowledge — remove from queue
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logging.info("Message acknowledged and removed from queue")

    except requests.exceptions.Timeout:
        failed_count += 1
        logging.error("FHIR server timeout — requeueing message")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    except requests.exceptions.ConnectionError:
        failed_count += 1
        logging.error("Cannot connect to FHIR server — requeueing message")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    except Exception as e:
        failed_count += 1
        logging.error(f"Unexpected error: {e} — requeueing message")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

# ------------------------------------------------
# START CONSUMER
# ------------------------------------------------
print("="*50)
logging.info("HL7 to FHIR Consumer Engine starting...")
logging.info("Connecting to RabbitMQ on localhost...")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)
channel = connection.channel()
channel.queue_declare(queue="hl7_queue", durable=True)
channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    queue="hl7_queue",
    on_message_callback=process_hl7_message
)

logging.info("Consumer ready — waiting for HL7 messages...")
logging.info("Press Ctrl+C to stop\n")

try:
    channel.start_consuming()
except KeyboardInterrupt:
    logging.info("Consumer stopped by user")
    logging.info(f"Final stats: Processed={processed_count} | Failed={failed_count}")
    connection.close()
    print("\nConsumer stopped cleanly.")