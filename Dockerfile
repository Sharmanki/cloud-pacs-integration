# Base image - official Python
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy your script
COPY fhir.py .

# Run the script when container starts
CMD ["python", "fhir.py"]