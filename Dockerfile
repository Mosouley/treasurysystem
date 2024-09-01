# Dockerfile

# pull official base image
FROM python:3.12.5-alpine 

# Create a non-privileged user
RUN adduser --system --group celeryuser

# # set work directory
# WORKDIR /treasurysystem

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # install dependencies
# RUN pip install --upgrade pip
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # COPY . .
# # Copy project
# COPY . /treasurysystem/

# # Create static directory if it doesn't exist
# RUN mkdir -p /treasurysystem/static
# # Set permissions
# RUN chown -R celeryuser:celeryuser /treasurysystem

# # Set the non-privileged user to run subsequent commands
# USER celeryuser

# # Default command to run (can be overridden in docker-compose)
# CMD ["celery", "-A", "treasurysystem", "worker", "-l", "info"]

# Use a specific and slim base image for smaller size and consistency
FROM python:3.11-slim

# Create a non-privileged user and install dependencies
RUN adduser --system --group celeryuser && \
    pip install --upgrade pip && \
    mkdir -p /treasurysystem/static

# Set work directory
WORKDIR /treasurysystem

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies (leveraging Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /treasurysystem/

# Set permissions
RUN chown -R celeryuser:celeryuser /treasurysystem

# Set the non-privileged user to run subsequent commands
USER celeryuser

# Default command to run (can be overridden in docker-compose)
CMD ["celery", "-A", "treasurysystem", "worker", "-l", "info"]
