from flask import Flask,render_template, request,redirect,url_for,send_from_directory
import cv2
import os

app = Flask(__name__)

UPLOAD_FOLDER ="uploads/"
OUTPUT_FOLDER = "output/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER,exist_ok=True)
os.makedirs(OUTPUT_FOLDER,exist_ok=True)

def convert_to_sketch(image_path,output_path):
    img = cv2.imread(image_path)
    gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    inverted_gray_img = 255 - gray_img
    blurred_img = cv2.GaussianBlur(inverted_gray_img,(21,21),0)
    inverted_blur = 255 - blurred_img
    sketch_img = cv2.divide(gray_img, inverted_blur , scale=256.0)
    cv2.imwrite(output_path,sketch_img)
@app.route('/', methods=['GET','POST'])
def design():
    if request.method == "POST":
        if "image" not in request.files:
            return "No file Uploaded",400
        file = request.files["image"]
        if file.filename == "":
            return "No file selected",400
        
        filepath = os.path.join(app.config["UPLOAD_FOLDER"],file.filename)
        file.save(filepath)

        output_filename = f"sketch_{file.filename}"
        output_filepath = os.path.join(app.config["OUTPUT_FOLDER"],output_filename)
        convert_to_sketch(filepath,output_filepath)
        return render_template("design.html",sketch_filename=output_filename)
    
    return render_template("design.html",sketch_filename=None)
@app.route("/ouput/<filename>")
def output_file(filename):
    return send_from_directory(app.config["OUTPUT_FOLDER"],filename)



if __name__ == '__main__':
    app.run(debug=True)
