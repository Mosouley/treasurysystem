# Dockerfile

# pull official base image
FROM python:3

# set work directory
WORKDIR /treasurysystem

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy entrypoint.sh
# COPY entrypoint.sh .
# RUN sed -i 's/\r$//g' /treasurysystem/entrypoint.sh
# RUN chmod +x /treasurysystem/entrypoint.sh
# Mounts the application code to the image
# copy project
COPY . .

# run entrypoint.sh
# ENTRYPOINT ["/treasurysystem/entrypoint.sh"]
# EXPOSE 8000

# runs the production server
# ENTRYPOINT ["python", "treasurysystem/manage.py"]
# CMD ["runserver", "0.0.0.0:8000"]