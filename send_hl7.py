import socket

# MLLP framing characters
VT  = b'\x0b'   # start of block
FS  = b'\x1c'   # end of block  
CR  = b'\x0d'   # carriage return

# Raw HL7 ADT message
hl7_message = (
    "MSH|^~\\&|HIS|TORONTO_GEN|MIRTH|FHIR|20240415||ADT^A01|MSG001|P|2.5\r"
    "PID|1||99999^^^MRN||KUMAR^ANKIT||19900315|M|||123 Main St^^Toronto^ON^M5V1A1^CA\r"
    "PV1|1|I|RAD^101^A|||Dr.Smith|||RAD"
)

# Wrap in MLLP frame
mllp_message = VT + hl7_message.encode() + FS + CR

# Send to Mirth Connect on port 6661
print("Sending HL7 message to Mirth Connect...")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 6661))
sock.send(mllp_message)

# Receive acknowledgement
response = sock.recv(4096)
print("Mirth ACK received:")
print(response.decode().strip())
sock.close()

print("\nDone! Check Mirth dashboard for received message.")