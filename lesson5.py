# Lesson 5 - If/Else
# Decision making in integration logic

# ------------------------------------------------
# 1. BASIC if/else
# ------------------------------------------------
gender_hl7 = "M"

if gender_hl7 == "M":
    print("male")
else:
    print("female")

# ------------------------------------------------
# 2. if/elif/else - multiple conditions
# HL7 gender codes: M, F, U (unknown), A (ambiguous)
# ------------------------------------------------
gender_code = "U"

if gender_code == "M":
    fhir_gender = "male"
elif gender_code == "F":
    fhir_gender = "female"
elif gender_code == "U":
    fhir_gender = "unknown"
else:
    fhir_gender = "other"

print(fhir_gender)

# ------------------------------------------------
# 3. Checking HTTP response codes
# This is exactly what we do after posting to FHIR
# ------------------------------------------------
status_code = 201

if status_code == 201:
    print("Success - Patient created on FHIR server")
elif status_code == 400:
    print("Error - Bad request, check your FHIR resource")
elif status_code == 422:
    print("Error - FHIR validation failed")
else:
    print("Unknown response: " + str(status_code))

# ------------------------------------------------
# 4. Checking if a field is empty
# HL7 fields are often empty - must handle this
# ------------------------------------------------
pid_field = ""

if pid_field == "":
    print("Field is empty - skipping")
else:
    print("Field value: " + pid_field)

# ------------------------------------------------
# 5. AND / OR - combining conditions
# ------------------------------------------------
is_admitted = True
has_mrn = True

if is_admitted and has_mrn:
    print("Patient ready to process")

age = 17
is_emergency = True

if age < 18 or is_emergency:
    print("Requires special handling")

# ------------------------------------------------
# 6. Real world - checking HL7 segment type
# and processing accordingly
# ------------------------------------------------
segments = [
    "MSH|^~\\&|HIS|TORONTO_GEN|FHIR|TEST|20240415",
    "PID|1||12345^^^MRN||KUMAR^ANKIT||19900315|M",
    "PV1|1|I|RAD^101^A|||Dr.Smith|||RAD"
]

for seg in segments:
    if seg.startswith("MSH"):
        print("Found header segment - MSH")
    elif seg.startswith("PID"):
        print("Found patient segment - PID - will parse")
    elif seg.startswith("PV1"):
        print("Found visit segment - PV1")
    else:
        print("Unknown segment - skipping")


message_type = "ORM"

if message_type == "ADT":
    print("Admission message")
elif message_type == "ORM":
    print("Radiology order message")
elif message_type == "ORU":
    print("Lab result message")
else:
    print("Unknown message type")

mrn = "12345"
if mrn == "":
    print("No MRN found")
else:
    print ("Processin MRN: " + mrn)

patient_name = "Ankit Kumar"
status_code = 201

if patient_name != "" and status_code == 201:
    print("Patient successfully sent to FHIR server")
