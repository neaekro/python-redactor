"""
BSD 3-Clause License

Copyright (c) 2021, Tyler Sameshima (tysameshima@gmail.com), Jay Ni (jay.ni.2001@gmail.com)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
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
            return jsonify(error="error, no file")
        file = request.files['file']
        if file.filename == '':
            return jsonify(error="error, no file name")
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            filestr = file.read()
            npimg = numpy.fromstring(filestr, numpy.uint8)
            boxes = detector.get_bounding_boxes(npimg)
            boxes = sorted(boxes, key=lambda box: box[0])
            text = []
            for (startX, startY, endX, endY) in boxes:
                text.append(preprocessor.process(detector.crop_image(npimg, startX, startY, endX, endY)))
            return jsonify(boxes=boxes, text=text)
        else:
            return jsonify(error="error, not accepted file format")


if __name__ == "__main__":
    app.run()
