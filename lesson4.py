# Lesson 4 - Dictionaries
# The backbone of FHIR resource building

# ------------------------------------------------
# 1. CREATING a dictionary
# key: value pairs, separated by commas
# ------------------------------------------------
patient = {
    "mrn":        "12345",
    "first_name": "Ankit",
    "last_name":  "Kumar",
    "dob":        "1990-03-15",
    "gender":     "male"
}
print(patient)

# ------------------------------------------------
# 2. ACCESSING values by key
# ------------------------------------------------
print(patient["mrn"])
print(patient["first_name"])
print(patient["gender"])

# ------------------------------------------------
# 3. ADDING a new key-value pair
# ------------------------------------------------
patient["admitted"] = True
patient["ward"] = "Radiology"
print(patient)

# ------------------------------------------------
# 4. UPDATING an existing value
# ------------------------------------------------
patient["ward"] = "ICU"
print(patient["ward"])

# ------------------------------------------------
# 5. CHECKING if a key exists
# ------------------------------------------------
print("mrn" in patient)       # True
print("passport" in patient)  # False

# ------------------------------------------------
# 6. LOOPING through a dictionary
# ------------------------------------------------
print("--- Patient Details ---")
for key, value in patient.items():
    print(key + ": " + str(value))

# ------------------------------------------------
# 7. NESTED dictionary
# Dictionary inside a dictionary
# This is how FHIR resources are structured
# ------------------------------------------------
fhir_patient = {
    "resourceType": "Patient",
    "identifier": [
        {"system": "urn:mrn", "value": "12345"}
    ],
    "name": [
        {
            "family": "Kumar",
            "given":  ["Ankit"]
        },
        {
            "family": "Rathod",
            "given":  ["Akanxi"]

        }
    ],
    "gender":    "male",
    "birthDate": "1990-03-15"
}

# Accessing nested values
print(fhir_patient["resourceType"])
for patients in fhir_patient:
    print(patients)
print(fhir_patient["name"][1]["family"])
print(fhir_patient["name"][1]["given"][0])
print(fhir_patient["identifier"][0]["value"])

# ------------------------------------------------
# 8. Converting dictionary to JSON string
# This is what gets sent to the FHIR server
# ------------------------------------------------
import json
fhir_json = json.dumps(fhir_patient, indent=2)
print(fhir_json)


hl7_message = {

"type" : "ADT^A01",
"sending_facility" : "Toronto General",
"receiving_facility" : "FHIR Server",
"datetime" : "20240415"
}

print(hl7_message["type"])
hl7_message["version"] = "2.5"
print(hl7_message)

for key, value in hl7_message.items():
    print(key +": " + str(value))

