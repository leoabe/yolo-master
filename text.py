import cv2
import numpy as np
import requests
import io
import json
from gtts import gTTS
import os


#OCR
#camera = cv2.VideoCapture(0)

#return_value, image = camera.read()
#cv2.imwrite('screenshot'+'.jpg', image)
#del(camera)

img = cv2.imread("screenshot.jpg")

height, width, _ = img.shape

#height=640
#width=480

# Cutting image
# roi = img[0: height, 400: width]
roi = img

# Ocr
url_api = "https://api.ocr.space/parse/image"
_, compressedimage = cv2.imencode(".jpg", roi, [1, 90])
file_bytes = io.BytesIO(compressedimage)

result = requests.post(url_api,
              files = {"screenshot.jpg": file_bytes},
              data = {"apikey": "6e8fdbcf4d88957",
                      "language": "eng"})

result = result.content.decode()
result = json.loads(result)

parsed_results = result.get("ParsedResults")[0]
text_detected = parsed_results.get("ParsedText")

text_file = open("sample.txt", "w")
n = text_file.write(text_detected)
text_file.close()

print(text_detected)

cv2.imshow("roi", roi)
cv2.imshow("Img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()



#TEXT TO SPEECH



fh = open("sample.txt", "r")
myText = fh.read().replace("\n", " ")

language = 'en'

output = gTTS(text=myText, lang=language, slow=False)

output.save("output.mp3")
fh.close()

os.system("start output.mp3")