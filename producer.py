# producer.py
# Simulates a hospital sending HL7 messages to a queue
# Like a HIS/RIS firing ADT messages all day long

import pika
import json
import time

# HL7 messages to send (simulating 3 hospital events)
hl7_messages = [
    "MSH|^~\\&|HIS|TORONTO_GEN|FHIR|TEST|20240415||ADT^A01|MSG001|P|2.5\rPID|1||12345^^^MRN||KUMAR^ANKIT||19900315|M",
    "MSH|^~\\&|HIS|TORONTO_GEN|FHIR|TEST|20240415||ADT^A01|MSG002|P|2.5\rPID|1||67890^^^MRN||SMITH^JOHN||19850520|M",
    "MSH|^~\\&|HIS|TORONTO_GEN|FHIR|TEST|20240415||ADT^A01|MSG003|P|2.5\rPID|1||11111^^^MRN||JOHNSON^SARA||19920710|F"
]

# Connect to RabbitMQ
print("Connecting to RabbitMQ...")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)
channel = connection.channel()

# Create the queue if it doesn't exist
# durable=True means queue survives RabbitMQ restart
channel.queue_declare(queue="hl7_queue", durable=True)

print("Connected! Sending HL7 messages...\n")

# Send each message to the queue
for i, message in enumerate(hl7_messages):
    channel.basic_publish(
        exchange="",
        routing_key="hl7_queue",
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2  # Make message persistent
        )
    )
    print(f"Sent message {i+1}: {message[45:65]}...")
    time.sleep(1)  # 1 second between messages

print("\nAll messages sent to queue!")
connection.close()