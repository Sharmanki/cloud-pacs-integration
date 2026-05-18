# consumer.py
# Reads HL7 messages from queue and transforms to FHIR
# Like your integration engine processing hospital messages

import pika
import json
import requests

def parse_pid(pid_segment):
    fields = pid_segment.split("|")
    mrn         = fields[3].split("^")[0]
    family_name = fields[5].split("^")[0]
    given_name  = fields[5].split("^")[1]
    dob_raw     = fields[7]
    gender_raw  = fields[8]
    dob = dob_raw[0:4] + "-" + dob_raw[4:6] + "-" + dob_raw[6:8]
    gender = "male" if gender_raw == "M" else "female"
    return {
        "mrn": mrn,
        "family": family_name,
        "given": given_name,
        "birthDate": dob,
        "gender": gender
    }

def build_fhir_patient(patient):
    return {
        "resourceType": "Patient",
        "identifier": [{"system": "urn:mrn", "value": patient["mrn"]}],
        "name": [{"family": patient["family"], "given": [patient["given"]]}],
        "birthDate": patient["birthDate"],
        "gender": patient["gender"]
    }

def process_hl7_message(ch, method, properties, body):
    print("\n--- New message received from queue ---")
    raw_hl7 = body.decode()

    # Parse segments
    segments = raw_hl7.strip().split("\r")
    pid_seg = None
    for seg in segments:
        if seg.startswith("PID"):
            pid_seg = seg
            break

    if not pid_seg:
        print("No PID segment found - skipping")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    # Transform to FHIR
    patient = parse_pid(pid_seg)
    fhir_patient = build_fhir_patient(patient)
    print(f"Transformed: {patient['given']} {patient['family']} | {patient['gender']}")

    # Post to FHIR server
    response = requests.post(
        "https://hapi.fhir.org/baseR4/Patient",
        headers={"Content-Type": "application/fhir+json"},
        json=fhir_patient
    )
    print(f"FHIR Server Response: {response.status_code}")
    print(f"Patient ID assigned: {response.json().get('id', 'unknown')}")

    # Acknowledge message — tells RabbitMQ it was processed successfully
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Message acknowledged and removed from queue")

# Connect to RabbitMQ
print("Consumer started — waiting for HL7 messages...")
print("Press Ctrl+C to stop\n")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)
channel = connection.channel()

# Same queue as producer
channel.queue_declare(queue="hl7_queue", durable=True)

# Only process one message at a time
channel.basic_qos(prefetch_count=1)

# Start listening
channel.basic_consume(
    queue="hl7_queue",
    on_message_callback=process_hl7_message
)

channel.start_consuming()