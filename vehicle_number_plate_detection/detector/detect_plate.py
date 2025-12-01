import cv2
import easyocr
import numpy as np
import os

reader = easyocr.Reader(['en'])

def detect_number_plate(image_path):
   
    img = cv2.imread(image_path)
    if img is None:
        return None, "Invalid image path!"

   
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)

  
    edges = cv2.Canny(blur, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    plate = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:  
            x, y, w, h = cv2.boundingRect(contour)
            plate = img[y:y+h, x:x+w]
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 3)
            break

    if plate is None:
        return None, "No plate detected"

    result = reader.readtext(plate)
    text = " ".join([d[1] for d in result])


    output_path = os.path.join('static', 'uploads', 'output.jpg')
    cv2.imwrite(output_path, img)

    return text, output_path
