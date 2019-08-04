"""
Main app script that calls everything
"""

from flask import Flask, render_template, request, redirect, url_for
import json, subprocess

application = Flask(__name__)

@application.route("/")
def welcome():
    return render_template("welcome.html")

@application.route("/generate")
def generate():
    return render_template("generate.html")


@application.route("/read")
def read():
    user = {'username': 'Jessica'}
    posts = [
        {
            'author': {'username': 'Sally'},
            'body': 'Beautiful day in Detroit!'
        },
        {
            'author': {'username': 'Mark'},
            'body': 'The Avengers movie sucked!'
        }
    ]
    return render_template("index.html", title='', user=user, posts=posts)

@application.route("/database")
def database():
    user = {'username': 'Tammy'}
    posts = [
        {
            'author': {'username': 'Sally'},
            'body': 'Beautiful day in Detroit!'
        },
        {
            'author': {'username': 'Mark'},
            'body': 'The Avengers movie sucked!'
        }
    ]
    return render_template("index.html", title='', user=user, posts=posts)

@application.route("/businesscard")
def businesscard():
    return render_template("businesscard.html")


@application.route('/thankyou')
def thankyou():
    return render_template("thankyou.html")

@application.route('/receiver', methods=['POST'])
def receiver():
    default_name = '0'
    fn = request.form.get('fn', default_name)
    occ = request.form.get('occ', default_name)
    ea = request.form.get('ea', default_name)
    pn = request.form.get('pn', default_name)
    web = request.form.get('web', default_name)
    fp = request.form.get('fp', default_name)
    op = request.form.get('op', default_name)
    pt = request.form.get('pt', default_name)

    imag = qrgenerator(pt, fn, fp, op, occ, ea, pn, web)
    subprocess.call(['open', str(op)])
    return 'Success'

"""
QRCode generator for business cards.
Parameters: postyp = <1 or 2>
            data   = <dict provided by user>
            imag   = <image for background or center>
            outpt  = <where to save the image>
08-01-2019
"""

def qrgenerator(postyp, fn, imag, outpt, occ, ea, pn, web):

#can change the position, pos1=bottom right, pos2=image at center
    postype  = int(postyp)
    img_path = str(imag)
    outpt    = str(outpt)

    #create the formatted output for the qr text
    arr =  { 'name': fn,
       'occupation': occ,
            'email': ea,
            'phone': pn,
            'url': web
            }
    text = 'Name:  {0[name]} \n Occupation: {0[occupation]} \n Email: {0[email]} \n Phone: {0[phone]} \n URL: {0[url]}'.format(arr)

    if postype not in [1,2]:
        print('ERROR: Postion type has to be either 1 (bottom right) or 2 (image at center)!')
        sys.exit()

    if postype == 1:
        try:
            img_bg = Image.open(img_path)
        except:
            print('ERROR: Image not found!')
            sys.exit()

        qr = qrcode.QRCode(box_size=2)
        qr.add_data(text)
        qr.make()
        img_qr = qr.make_image()

        pos = (img_bg.size[0] - img_qr.size[0], img_bg.size[1] - img_qr.size[1])
        img_bg.paste(img_qr, pos)
        img_bg.save(outpt)

    if postype == 2:
        try:
            face = Image.open(img_path)
        except:
            print('ERROR: Image not found!')
            sys.exit()

        (width, height) = (50, 50)
        face =face.resize((width, height))

        qr_big = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr_big.add_data(text)
        qr_big.make()
        img_bg = qr_big.make_image().convert('RGB')

        pos = ((img_bg.size[0] - face.size[0]) // 2, (img_bg.size[1] - face.size[1]) // 2)

        img_bg.paste(face, pos)
        img_bg.save(outpt)

    return img_bg

##---------------------------------------------------------------------------------------------------------------
#Testing the function
keys = 'N'
if keys == 'Y':
    arr =  { 'name': 'Christopher B. Johnson',
    'occupation':'Data Scientist/Developer',
            'url': 'https://cjohnson3585.github.io/r3/',
            'email': 'cbj3585@gmail.com',
            'phone':'586-718-4381',
            'cv': 'CV.PDF'}
    text = 'Name:  {0[name]} \n Occupation: {0[occupation]} \n Url:  {0[url]} \n Email: {0[email]} \n Phone: {0[phone]} \n CV: {0[cv]}'.format(arr)
    print(text)

    qrgenerator(1, text, './images/test_img.jpg', './images/qrcode.png')
    subprocess.call(['open','./images/qrcode.png'])

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000)
