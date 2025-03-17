
# Use an official Python runtime as a parent image
FROM python:3.10

COPY requirements.txt /app/  
WORKDIR /app  
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /main_script

RUN pip install --upgrade pip setuptools wheel

RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PORT=5000

# Expose the port Render will use
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]
