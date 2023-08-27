# Official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy application code into container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Command to run application
CMD ["python", "src/main.py"]

# Exposing Prometheus metrics port
EXPOSE 9090