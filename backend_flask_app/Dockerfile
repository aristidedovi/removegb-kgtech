# Use an official Python runtime as the base image
FROM python:3.11.9

# Set the working directory in the container
WORKDIR /backend-app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose port 5000 for the Flask app
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_CONFIG='production'

# Run the Flask app when the container starts
#CMD ["flask", "run", "--host=0.0.0.0", "--cert=cert.pem", "--key=key.pem"] 
CMD ["flask", "run", "--host=0.0.0.0"]         