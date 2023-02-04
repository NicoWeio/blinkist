 # Little tut:
 # Build image: docker build . -t blinkist
 # Run image: docker run --rm -it -v /Users/<user>/Desktop/dailyblink:/library blinkist --freedaily /library
 
 FROM python:3.10-alpine
 COPY . /app/
 RUN pip install --requirement /app/requirements.txt
 WORKDIR /app
 ENTRYPOINT ["python", "main.py"]
