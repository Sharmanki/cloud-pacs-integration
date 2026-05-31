# producer.py
import pika
import time
import random

# Generate unique run ID so every run creates fresh patients
run_id = random.randint(1000, 9999)

hl7_messages = [
    f"MSH|^~\\&|HIS|TORONTO_GEN|FHIR|TEST|20240415||ADT^A01|MSG001|P|2.5\rPID|1||{run_id}1^^^MRN||KUMAR^ANKIT{run_id}||19900315|M",
    f"MSH|^~\\&|HIS|TORONTO_GEN|FHIR|TEST|20240415||ADT^A01|MSG002|P|2.5\rPID|1||{run_id}2^^^MRN||SMITH^JOHN{run_id}||19850520|M",
    f"MSH|^~\\&|HIS|TORONTO_GEN|FHIR|TEST|20240415||ADT^A01|MSG003|P|2.5\rPID|1||{run_id}3^^^MRN||JOHNSON^SARA{run_id}||19920710|F"
]

print(f"Run ID: {run_id} — sending unique patients this session")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)
channel = connection.channel()
channel.queue_declare(queue="hl7_queue", durable=True)

print("Connected! Sending HL7 messages...\n")

for i, message in enumerate(hl7_messages):
    channel.basic_publish(
        exchange="",
        routing_key="hl7_queue",
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )
    print(f"Sent message {i+1} | Run ID: {run_id}")
    time.sleep(1)

print("\nAll messages sent to queue!")
connection.close()