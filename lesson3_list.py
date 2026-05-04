# Lesson 3 - Lists
# Critical for HL7 segment parsing and FHIR resources

# ------------------------------------------------
# 1. CREATING a list
# ------------------------------------------------
# A simple list of HL7 segment names
segments = ["MSH", "PID", "PV1", "OBR", "OBX"]
print(segments)

# ------------------------------------------------
# 2. ACCESSING items by index
# Index always starts at 0 in Python
# ------------------------------------------------
print(segments[0])    # first item  -> MSH
print(segments[1])    # second item -> PID
print(segments[-1])   # last item   -> OBX

# ------------------------------------------------
# 3. LENGTH of a list
# ------------------------------------------------
print(len(segments))  # 5 items

# ------------------------------------------------
# 4. ADDING items to a list
# ------------------------------------------------
segments.append("PV2")
print(segments)

# ------------------------------------------------
# 5. CHECKING if item exists in list
# ------------------------------------------------
print("PID" in segments)   # True
print("ZZZ" in segments)   # False

# ------------------------------------------------
# 6. LOOPING through a list
# This is how we process multiple HL7 segments
# ------------------------------------------------
print("--- All segments ---")
for segment in segments:
    print(segment)

# ------------------------------------------------
# 7. REAL WORLD - splitting HL7 into segment list
# ------------------------------------------------
raw_hl7 = ("MSH|^~\\&|HIS|TORONTO_GEN|FHIR|TEST|20240415||ADT^A01|MSG001|P|2.5\r"
           "PID|1||12345^^^MRN||KUMAR^ANKIT||19900315|M\r"
           "PV1|1|I|RAD^101^A|||Dr.Smith|||RAD")

hl7_segments = raw_hl7.strip().split("\r")
print("--- HL7 Segments ---")
for seg in hl7_segments:
    print(seg)

# ------------------------------------------------
# 8. FHIR list - exactly how FHIR JSON is built
# ------------------------------------------------
given_names = ["Ankit", "Kumar"]   # a patient can have multiple given names
print(given_names)
print(given_names[0])   # first given name

# ------------------------------------------------
# 9. LIST of DICTIONARIES - the real FHIR structure
# Don't worry too much about this yet - 
# we cover dictionaries in Lesson 4
# ------------------------------------------------
identifiers = [
    {"system": "urn:mrn",         "value": "12345"},
    {"system": "urn:healthcard",  "value": "ON9876543"}
]
print(identifiers[0])           # first identifier
print(identifiers[0]["value"])  # value of first identifier


hl7_message_types = ["ADT", "ORM", "ORU", "ACK"]
print(hl7_message_types)
print(hl7_message_types[2])
hl7_message_types.append("SIU")
print(len(hl7_message_types))

for hl7_message_type in hl7_message_types:
    print("types: " + hl7_message_type)