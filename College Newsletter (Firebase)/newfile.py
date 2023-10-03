from flask import Flask, render_template, send_from_directory
import os,sys
import firebase_admin
from firebase_admin import credentials,storage
import numpy as np
import cv2

app = Flask(__name__)
cred = credentials.Certificate("key.json")
cloud= firebase_admin.initialize_app(cred,{'storageBucket':'newsletter-280923.appspot.com'})
bucket=storage.bucket()
images = os.listdir("static/images")
for i in range(1,6):
    blob=bucket.get_blob(f"image ({i}).jpg")

    if(f"image ({i}).jpg") in images:
        continue;
    print(type(blob))
    arr=np.frombuffer(blob.download_as_string(),np.uint8)
    img=cv2.imdecode(arr,cv2.COLOR_BGR2BGR555)
    cv2.imwrite(f"static/images/image ({i}).jpg",img)
images = os.listdir("static/images")

@app.route("/")
def home():
    return render_template("home.html", images=images)

@app.route("/images/<filename>")
def get_image(filename):
    return send_from_directory("static/images", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
