# Use an official Python runtime as base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt from the project root into the container
COPY requirements.txt /app/

# Copy the app folder (main script)
COPY app /app/

# Copy the templates folder separately
COPY templates /app/templates/

# Copy CSS and JS files separately
COPY style.css /app/static/style.css
COPY script.js /app/static/script.js

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask app
EXPOSE 5000

# Command to run the correct script
CMD ["python", "main_script.py"]

