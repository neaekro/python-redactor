from flask import Flask, request, jsonify
import numpy
import detector
import preprocessor

app = Flask(__name__)
ALLOWED_EXTENSIONS = ['jpg', 'png', 'jpeg']


@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "error, no file"
        file = request.files['file']
        if file.filename == '':
            return "error, no file name"
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            filestr = file.read()
            npimg = numpy.fromstring(filestr, numpy.uint8)
            boxes = detector.get_bounding_boxes(npimg)
            if boxes == "error":
                return jsonify(error="an error has occurred")
            text = []
            for (startX, startY, endX, endY) in boxes:
                text.append(preprocessor.process(detector.crop_image(npimg, startX, startY, endX, endY)))
            return jsonify(boxes=boxes, text=text)
        else:
            return "error, not accepted file format"


if __name__ == "__main__":
    app.run()