FROM python:latest

ADD server.py .
ADD detector.py .
ADD preprocessor.py .
ADD frozen_east_text_detection.pb .

RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install Flask opencv-python numpy pytesseract
EXPOSE 5000

CMD [ "python", "./server.py" ]