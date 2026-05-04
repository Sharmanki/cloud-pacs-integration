# Lesson 2 - Strings
# The most important lesson for HL7 parsing

# Define a raw HL7 PID segment as a string
pid_segment = "PID|1||12345^^^MRN||KUMAR^ANKIT||19900315|M"

# ------------------------------------------------
# 1. LENGTH - how many characters in the string
# ------------------------------------------------
print(len(pid_segment))

# ------------------------------------------------
# 2. SLICING - extract part of a string by position
# HL7 date "19900315" -> we need "1990-03-15"
# ------------------------------------------------
dob_raw = "19900315"
year  = dob_raw[0:4]   # characters 0,1,2,3
month = dob_raw[4:6]   # characters 4,5
day   = dob_raw[6:8]   # characters 6,7

print(year)
print(month)
print(day)
print(year + "-" + month + "-" + day)

# ------------------------------------------------
# 3. SPLIT - break a string into a list
# This is how we parse HL7 pipe-delimited segments
# ------------------------------------------------
fields = pid_segment.split("|")
print(fields)
print(fields[3])    # PID.3 = MRN field
print(fields[8])    # PID.8 = Gender field

# ------------------------------------------------
# 4. SPLIT again on ^ to get sub-fields
# PID.5 = "KUMAR^ANKIT" -> ["KUMAR", "ANKIT"]
# ------------------------------------------------
name_field  = fields[5]
name_parts  = name_field.split("^")
family_name = name_parts[0]
given_name  = name_parts[1]

print(family_name)
print(given_name)

# ------------------------------------------------
# 5. UPPER and LOWER - change case
# ------------------------------------------------
print(family_name.upper())
print(family_name.lower())

# ------------------------------------------------
# 6. STRIP - remove extra spaces
# Real HL7 messages often have trailing spaces
# ------------------------------------------------
messy_value = "  KUMAR  "
print(messy_value.strip())

# ------------------------------------------------
# 7. REPLACE - swap one value for another
# ------------------------------------------------
gender_hl7  = "M"
gender_fhir = gender_hl7.replace("M", "male")
print(gender_fhir)

# ------------------------------------------------
# 8. STARTSWITH - check segment type
# This is how we find PID vs MSH vs PV1
# ------------------------------------------------
print(pid_segment.startswith("PID"))
print(pid_segment.startswith("MSH"))

MRN_Field = fields[3]
Get_MRN = MRN_Field.split("^")
MRN = Get_MRN[0]
print(MRN)

send_facility = "    TORONTO_GEN    "
FAC_STRIP = send_facility.strip()
print(FAC_STRIP.lower())

print(month +"-"+ day)