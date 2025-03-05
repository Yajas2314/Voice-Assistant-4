# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

pip install --upgrade pip

# Install any needed dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "main_script.py"]
