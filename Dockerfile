# Dockerfile

# pull official base image
FROM python:3

# Create a non-privileged user
RUN adduser --system --group celeryuser

# set work directory
WORKDIR /treasurysystem

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPY . .
# Copy project
COPY . /treasurysystem/

# Set permissions
RUN chown -R celeryuser:celeryuser /treasurysystem

# Set the non-privileged user to run subsequent commands
USER celeryuser

# Default command to run (can be overridden in docker-compose)
CMD ["celery", "-A", "treasurysystem", "worker", "-l", "info"]