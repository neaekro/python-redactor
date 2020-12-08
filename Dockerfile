FROM python:latest

ADD server.py .
ADD detector.py .
ADD preprocessor.py .
ADD frozen_east_text_detection.pb .

RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6 tesseract-ocr -y
RUN pip install Flask opencv-python numpy pytesseract
ENV FLASK_APP=server.py
EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]