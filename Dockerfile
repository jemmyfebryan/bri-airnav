# Use a base image with Python installed
FROM python:3.11.3-slim

# Ensure Python output is not buffered
ENV PYTHONBUFFERED True

# Set the application directory
ENV APP_HOME /app

# Set the working directory
WORKDIR $APP_HOME

# Install required system packages for OpenCV and OpenGL
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application using Gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
