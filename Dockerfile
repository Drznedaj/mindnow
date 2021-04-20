# Dockerfile

# Pull base image
FROM python:3.6

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /mindnow

COPY requirements.txt /tmp/requirements.txt
COPY geoip/ /usr/lib/geoip
# Install dependencies
RUN pip install -r /tmp/requirements.txt

# Copy project
ADD . /mindnow/