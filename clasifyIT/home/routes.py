from flask import Blueprint, render_template, jsonify, request,make_response,send_file
from keras.models import load_model
from PIL import Image
from .utlis import prepare_image
import numpy as np
import io 
import os
import base64
from flask_login import login_user, logout_user, current_user
from ..email import sender
from email.mime.text import MIMEText
from ..encrypt import des_ofb,hash

home = Blueprint('home', __name__)
model = load_model(os.path.join(os.getcwd(), "clasifyIT/FINAL.h5"))
model._make_predict_function()

@home.route('/')
def index():
    return render_template('index.html')


@home.route('/search-doctor')
def search():
    return render_template('search.html')

    
@home.route('/contact')
def contact():
    return render_template('contact.html')

@home.route("/download-pdf",methods=["POST"])
def createPdf():
    def randomString():
        import string, secrets
        nonlocal  password
        """Generate a random string of fixed length """
        password_characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(password_characters) for _ in range(10))

    from fpdf import FPDF
    message = request.get_json(force=True)
    pdf = FPDF()
    pdf.compress = True
    pdf.add_page()
    pdf.set_font('Arial', '', 14)
    pdf.ln(10)
    pdf.write(25, message['prediction'])
    print(pdf.output('py3k.pdf', 'F'))
    pdf.close()
    from PyPDF2 import PdfFileReader, PdfFileWriter
    with open("py3k.pdf", "rb") as in_file:
        password = 0
        input_pdf = PdfFileReader(in_file)
        output_pdf = PdfFileWriter()
        output_pdf.appendPagesFromReader(input_pdf)
        email=des_ofb.ofb_decrypt(current_user.email,current_user.password_hash[:8],current_user.password_hash[24:32])
        randomString()
        output_pdf.encrypt(password)
        out_file=open('encrypted_output.pdf', 'wb')
        out_file.seek(0)
        output_pdf.write(out_file)
        out_file.close()
        sender.SendMail().preapare_attatched_mail(email,"The password","Open the file to see the password for pdf",
                                                  password)
        return send_file("../encrypted_output.pdf",mimetype='application/pdf',as_attachment=True)

@home.route("/predict", methods=["POST"])
def predict():
    """
    prediction function that gets an image from the user (frontend upload)
    and classifies it with a pre-trained model
    :return:
    """
    if current_user.is_authenticated:
        message = request.get_json(force=True)
        encoded = message['image']
        decoded = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(decoded))
        processed_image = prepare_image(image, target_size=(50,50))#resizeing the image


        prediction = np.argmax(model.predict(processed_image).tolist())#getting the prediction

        cancer_type = { #translation dict
            0 : "Melanocytic_nevi",
            1 : "Melanoma",
            2 : "Benign_keratosis",
            3 : "Basal_cell_carcinoma",
            4 : "Actinic_keratoses",
            5 : "Vascular_lesions",
            6 : "Dermatofibroma"
        }
        prediction = cancer_type[prediction]

        email=des_ofb.ofb_decrypt(current_user.email,current_user.password_hash[:8],current_user.password_hash[24:32])  
        sender.SendMail().preapare_attatched_mail(email,"The Result","Open the file to see the result",prediction)


        # sending the result to the front
        response = {'prediction': {'result' : prediction}}
        return jsonify(response)
    else:
        return redirect(url_for('user.login')) #if not logged in redirecting to login page
