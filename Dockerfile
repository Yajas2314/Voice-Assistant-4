# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /main_script

# Copy the current directory contents into the container
COPY . /main_script

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PORT=5000

# Expose the port Render will use
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]
