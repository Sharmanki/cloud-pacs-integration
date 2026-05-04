# Lesson 1 - Variables and Data Types
# The # symbol means a comment - Python ignores this line

# String variables - text always goes in quotes
patient_name = "Ankit Kumar"
patient_mrn  = "12345"
gender       = "male"
birth_date   = "1990-03-15"
hospita_name = "Toronto General"

# Integer variables - numbers without quotes
port_number  = 6661
status_code  = 201
bed_number = 101

# Float variables - decimal numbers
temperature  = 98.6

# Boolean variables - only True or False
is_admitted  = True
is_discharged = False

# Print them to the screen
print(patient_name)
print(patient_mrn)
print(port_number)
print(is_admitted)

# Check what TYPE a variable is
print(type(patient_name))
print(type(port_number))
print(type(temperature))
print(type(is_admitted))

print(hospita_name)
print(bed_number)
print(patient_mrn + " - " + patient_name)