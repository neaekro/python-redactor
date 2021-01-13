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
import requests
import cv2
import numpy as np
import random
import textwrap

# select random dimensions between 512 and 2048 pixels, inclusive
width, height = random.randint(512, 2048), random.randint(512, 2048)

image = np.random.randint(255, size=(height, width, 3), dtype=np.uint8)
wrapped_text = textwrap.wrap("Hello World!", width=35)

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 3
fontColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
lineType = 2

for i, line in enumerate(wrapped_text):
    textsize = cv2.getTextSize(line, font, fontScale, lineType)[0]

    gap = textsize[1] + 10

    y = int((image.shape[0] + textsize[1]) / 2) + i * gap
    x = int((image.shape[1] - textsize[0]) / 2)

    cv2.putText(image, "Hello World!", (x, y), font, fontScale, fontColor, lineType)

cv2.imwrite("random.jpg".format(width = width, height = height), image)
files = {'file': open('random.jpg', 'rb')}
r = requests.post('http://localhost:5000', files=files)
print(r.status_code)
print(r.text)