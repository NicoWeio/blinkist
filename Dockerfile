# === BASIC USAGE ===
# Build image: docker build . -t blinkist
# Run image: docker run --rm -it -v /path/to/your/library:/data blinkist /data --freedaily
#   (adjust these parts:)           ^^^^^^^^^^^^^^^^^^^^^                      ^^^^^^^^^^^

FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --requirement requirements.txt
COPY . .
WORKDIR /data
ENTRYPOINT ["python3", "/app/main.py"]
