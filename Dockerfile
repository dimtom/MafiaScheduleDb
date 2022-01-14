FROM python:3.9-slim
# NB: also, consider python:3.9
# NB: also, consider python:3.9-alpine - directory structure is different

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn


WORKDIR /app

# copy .env file - it is ignored as it starts from .
COPY [".env", "/app"]

# copy everything to /app folder
COPY . /app



# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# enable port 8000
EXPOSE 8000

# run app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
