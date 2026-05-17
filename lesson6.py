# Lesson 6 - Loops
# Processing multiple HL7 messages like a real integration engine

# ------------------------------------------------
# 1. FOR loop - basic
# ------------------------------------------------
message_types = ["ADT", "ORM", "ORU", "ACK", "SIU"]

for msg_type in message_types:
    print("Processing: " + msg_type)

# ------------------------------------------------
# 2. FOR loop with index using enumerate
# Useful when you need the position number too
# ------------------------------------------------
print("--- With index ---")
for index, msg_type in enumerate(message_types):
    print(str(index) + ": " + msg_type)

# ------------------------------------------------
# 3. FOR loop with range
# Useful for repeating something N times
# ------------------------------------------------
print("--- Sending 3 test messages ---")
for i in range(3):
    print("Sending message " + str(i + 1) + " of 3")

# ------------------------------------------------
# 4. WHILE loop
# Keeps running until condition is False
# This is how a real HL7 listener works --
# it keeps listening until you stop it
# ------------------------------------------------
messages_to_process = 3
count = 0

while count < messages_to_process:
    print("Listening for message... received #" + str(count + 1))
    count = count + 1

print("All messages processed")

# ------------------------------------------------
# 5. Loop through HL7 segments - REAL WORLD
# This is exactly what our FHIR script did
# ------------------------------------------------
raw_hl7 = ("MSH|^~\\&|HIS|TORONTO_GEN|FHIR|TEST|20240415||ADT^A01|MSG001|P|2.5\r"
           "PID|1||12345^^^MRN||KUMAR^ANKIT||19900315|M\r"
           "PV1|1|I|RAD^101^A|||Dr.Smith|||RAD")

segments = raw_hl7.strip().split("\r")

for seg in segments:
    if seg.startswith("MSH"):
        print("Header found")
    elif seg.startswith("PID"):
        fields = seg.split("|")
        print("Patient: " + fields[5])
    elif seg.startswith("PV1"):
        print("Visit info found")

# ------------------------------------------------
# 6. Loop through multiple patients - BATCH
# In real life you process hundreds of messages
# ------------------------------------------------
patients = [
    {"mrn": "12345", "name": "Ankit Kumar",  "gender": "M"},
    {"mrn": "67890", "name": "John Smith",   "gender": "M"},
    {"mrn": "11111", "name": "Sara Johnson", "gender": "F"}
]

print("--- Processing patient batch ---")
for patient in patients:
    gender = "male" if patient["gender"] == "M" else "female"
    print("MRN: " + patient["mrn"] + " | Name: " + patient["name"] + " | FHIR Gender: " + gender)

# ------------------------------------------------
# 7. BREAK and CONTINUE
# break = stop the loop completely
# continue = skip this item, go to next
# ------------------------------------------------
print("--- Skipping empty MRNs ---")
mrn_list = ["12345", "", "67890", "", "11111"]

for mrn in mrn_list:
    if mrn == "":
        continue    # skip empty MRNs
    print("Processing MRN: " + mrn)

messages = [
    {"type": "ADT", "patient": "Ankit Kumar"},
    {"type": "ORM", "patient": "John Smith"},
    {"type": "ORU", "patient": "Sara Johnson"},
    {"type": "ADT", "patient": "Mike Brown"}
]

# Challenge 1
for message in messages:
    print("Message type: " + message["type"] + " | " + message["patient"])

# Challenge 2    
    if message["type"] != "ADT":
        continue
    print("Message type: " + message["type"] + " | " + message["patient"])

# Challenge 3
retry = 0
couter = 3
while retry < couter:
    print("Attempting connection... try #" + str(retry + 1))
    retry = retry + 1
    if retry == couter:
        break
print("Max retries reached - stopping")