# Dockerfile

# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /treasurysystem

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
# copy project
COPY . .

# EXPOSE 8000

# runs the production server
# ENTRYPOINT ["python", "treasurysystem/manage.py"]
# CMD ["runserver", "0.0.0.0:8000"]