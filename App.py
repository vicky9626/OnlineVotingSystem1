from flask import Flask, render_template, flash, request, session
from flask import render_template, redirect, url_for, request
import mysql.connector
import sys, fsdk, math, ctypes, time
import datetime
from ecies.utils import generate_key
from ecies import encrypt, decrypt
import base64, os
app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/Home")
def Home():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewCandidate")
def NewCandidate():
    return render_template('NewCandidate.html')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb")
            data = cur.fetchall()
            return render_template('AdminHome.html', data=data)

        else:
            return render_template('index.html', error=error)


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')

    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/candidate", methods=['GET', 'POST'])
def candidate():
    if request.method == 'POST':
        name = request.form['name']
        area = request.form['pcode']
        pname = request.form['pname']
        f = request.files['file']
        f.save("static/upload/" + f.filename)
        address = request.form['address']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
        cursor = conn.cursor()
        cursor.execute("insert into cantb value('','" + name + "','" + area + "','" + pname + "','" + f.filename + "','"+ address +"')")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')

        cur = conn.cursor()
        cur.execute("SELECT * FROM cantb")
        data = cur.fetchall()
        flash('Record Save..!')

        return render_template('AdminCanInfo.html', data=data)


@app.route("/uremove")
def uremove():
    did = request.args.get('did')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
    cursor = conn.cursor()
    cursor.execute("delete from regtb  where VoterId='" + did + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    data = cur.fetchall()
    flash('User Remove successfully..!')

    return render_template('AdminHome.html', data=data)


@app.route("/remove")
def remove():
    did = request.args.get('did')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
    cursor = conn.cursor()
    cursor.execute("delete from cantb  where Id='" + did + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cantb ")
    data = cur.fetchall()
    flash('Candidate Remove successfully..!')

    return render_template('AdminCanInfo.html', data=data)


@app.route("/AdminCanInfo")
def AdminCanInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')

    cur = conn.cursor()
    cur.execute("SELECT * FROM cantb")
    data = cur.fetchall()
    return render_template('AdminCanInfo.html', data=data)


@app.route("/AdminVoteInfo")
def AdminVoteInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM votedtb")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  count(*) as count  FROM votedtb ")
    data1 = cursor.fetchone()

    if data1:
        count = data1[0]
    else:
        return 'Incorrect username / password !'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')

    cur = conn.cursor()
    cur.execute("SELECT distinct PartCode FROM votedtb")
    party = cur.fetchall()

    return render_template('AdminVoteInfo.html', data=data, count=count, party=party)


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        party = request.form['party']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM votedtb where PartCode='" + party + "' ")
        data = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  count(*) as count  FROM votedtb where PartCode='" + party + "'")
        data1 = cursor.fetchone()

        if data1:
            count = data1[0]
        else:
            return 'Incorrect username / password !'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')

        cur = conn.cursor()
        cur.execute("SELECT distinct PartCode FROM votedtb")
        party = cur.fetchall()

        return render_template('AdminVoteInfo.html', data=data, count=count, party=party)


@app.route("/NewUser")
def NewUser():
    import LiveRecognition  as liv

    liv.att()
    del sys.modules["LiveRecognition"]
    return render_template('NewUser.html')


@app.route("/newuser", methods=['GET', 'POST'])
def NewStudent1():
    if request.method == 'POST':
        uname = request.form['uname']
        fname = request.form['fname']
        gender = request.form['gender']
        Age = request.form['Age']
        email = request.form['email']
        pnumber = request.form['pnumber']
        address = request.form['address']
        vid = request.form['vid']
        aid = request.form['aid']

        f = request.files['file']
        import random
        pn = random.randint(1111, 9999)
        f.save("static/upload/" + str(pn) + ".png")
        fnam = str(pn) + ".png"

        secp_k = generate_key()
        privhex = secp_k.to_hex()
        pubhex = secp_k.public_key.format(True).hex()

        filepath = "./static/upload/" + fnam
        head, tail = os.path.split(filepath)

        newfilepath1 = './static/Encrypt/' + str(tail)
        newfilepath2 = './static/Decrypt/' + str(tail)

        data = 0
        with open(filepath, "rb") as File:
            data = base64.b64encode(File.read())  # convert binary to string data to read file

        print("Private_key:", privhex, "\nPublic_key:", pubhex, "Type: ", type(privhex))

        if (privhex == 'null'):
            flash('Please Choose Another File,file corrupted!')
            return render_template('NewUser.html')

        else:
            print("Binary of the file:", data)
            encrypted_secp = encrypt(pubhex, data)
            print("Encrypted binary:", encrypted_secp)

            with open(newfilepath1, "wb") as EFile:
                EFile.write(base64.b64encode(encrypted_secp))
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
            cursor = conn.cursor()
            cursor.execute(
                "insert into regtb values('" + uname + "','" + fname + "','" + gender + "','" + Age + "','" + email + "','" +
                pnumber + "','" + address + "','" + vid + "','" + aid + "','" +
                fnam + "','"+ pubhex +"','"+ privhex +"')")
            conn.commit()
            conn.close()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb")
            data = cur.fetchall()
            flash('Record Save..!')

            return render_template("AdminHome.html", data=data)






@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        vid = request.form['vid']

        session['vid'] = vid

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where VoterId='" + vid + "' ")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('UserLogin.html')



        else:
            print(data[0])
            session['vid'] = data[7]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
            cursor = conn.cursor()
            cursor.execute("truncate table temptb")
            conn.commit()
            conn.close()

            return FingerVerify()

            # return render_template('OTP.html', data=data )


@app.route("/FingerVerify")
def FingerVerify():
    return render_template('FingerVerify.html')


import cv2
from skimage.metrics import structural_similarity as ssim


def image_compare(image1_path, image2_path):
    # Read the images
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # Convert images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Compute Structural Similarity Index (SSIM) between the two images
    similarity_index = ssim(gray1, gray2)

    return similarity_index


@app.route("/fingerve", methods=['GET', 'POST'])
def fingerve():
    if request.method == 'POST':
        vid = session['vid']

        f = request.files['file']
        import random
        pn = random.randint(1111, 9999)
        f.save("static/upload/" + str(pn) + ".png")
        img2 = str(pn) + ".png"

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where VoterId='" + vid + "' ")
        data = cursor.fetchone()
        if data:
            img1 = data[9]
            prkey = data[11]

            privhex = prkey

            filepath = "./static/Encrypt/" + img1
            head, tail = os.path.split(filepath)

            newfilepath1 = './static/Encrypt/' + str(tail)
            newfilepath2 = './static/Decrypt/' + str(tail)

            data = 0
            with open(newfilepath1, "rb") as File:
                data = base64.b64decode(File.read())

            print(data)
            decrypted_secp = decrypt(privhex, data)
            print("\nDecrypted:", decrypted_secp)
            with open(newfilepath2, "wb") as DFile:
                DFile.write(base64.b64decode(decrypted_secp))

        img1 = newfilepath2

        img2 = "static/upload/" + img2
        try:
            similarity_index = image_compare(img1, img2)
            print(similarity_index)
        except:
            similarity_index = 0

        if int(similarity_index) == 1.0:
            import LiveRecognition1  as liv1
            del sys.modules["LiveRecognition1"]

            return Vote1()

        else:
            flash('Finger Image Incorrect..!')
            return render_template('FingerVerify.html')



def examvales1():
    vid = session['vid']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM regtb where  VoterId='" + vid + "'")
    data = cursor.fetchone()

    if data:
        Email = data[4]
        Phone = data[5]
        session['address'] = data[6]

    else:
        return 'Incorrect username / password !'

    return vid, Email, Phone


@app.route("/Vote1")
def Vote1():
    vid = session['vid']
    address = session['address']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * from temptb where UserName='" + vid + "' ")
    data = cursor.fetchone()
    if data is None:

        flash('Face  is wrong')
        return render_template('UserLogin.html')



    else:

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')

        cur = conn.cursor()
        cur.execute("SELECT * FROM cantb")
        data = cur.fetchall()

        return render_template('OTP.html', data=data)


@app.route("/otp", methods=['GET', 'POST'])
def otp():
    if request.method == 'POST':
        otp = request.form['vid']

        # session['vid'] = vid
        address = session['address']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from temptb where Status='" + otp + "' ")
        data = cursor.fetchone()
        if data is None:

            flash('OTP Incorrect')
            render_template('OTP.html')



        else:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')

            cur = conn.cursor()
            cur.execute("SELECT * FROM cantb where Address='"+ address +"'")
            data = cur.fetchall()

            return render_template('Vote.html', data=data)


@app.route("/Vote")
def Vote():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')

    cur = conn.cursor()
    cur.execute("SELECT * FROM cantb")
    data = cur.fetchall()
    return render_template('Vote.html', data=data)


import hmac
import hashlib
import binascii
import random


def create_sha256_signature(key, message):
    byte_key = binascii.unhexlify(key)
    message = message.encode()
    return hmac.new(byte_key, message, hashlib.sha256).hexdigest().upper()


@app.route("/uvote")
def uvote():
    did = request.args.get('did')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM cantb where  id='" + did + "'")
    data = cursor.fetchone()

    if data:
        PartCode = data[3]
        image = data[4]



    else:
        return 'Incorrect username / password !'

    vid = session['vid']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * from votedtb where VoterId='" + vid + "' ")
    data = cursor.fetchone()
    if data is None:

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM votedtb ")
        data = cursor.fetchone()

        if data:

            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
            cursor1 = conn1.cursor()
            cursor1.execute("select max(id) from votedtb")
            da = cursor1.fetchone()
            if da:
                d = da[0]
                print(d)

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
            cursor = conn.cursor()
            cursor.execute("SELECT  *  FROM votedtb where  id ='" + str(d) + "'   ")
            data = cursor.fetchone()
            if data:
                hash1 = data[6]
                num1 = random.randrange(1111, 9999)
                hash2 = create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", str(num1))

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
                cursor = conn.cursor()
                cursor.execute(
                    "insert into votedtb value('','" + vid + "','" + PartCode + "','" + image + "','1','" + hash1 + "','" + hash2 + "')")
                conn.commit()
                conn.close()

                flash('Vote Completed!')
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
                cur = conn.cursor()
                cur.execute("SELECT * FROM cantb")
                data = cur.fetchall()
                return render_template('Vote.html', data=data)

        else:

            hash1 = '0'
            num1 = random.randrange(1111, 9999)
            hash2 = create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", str(num1))

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
            cursor = conn.cursor()
            cursor.execute(
                "insert into votedtb value('','" + vid + "','" + PartCode + "','" + image + "','1','" + hash1 + "','" + hash2 + "')")
            conn.commit()
            conn.close()

            flash('Vote Completed!')
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3facefingervoteencdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM cantb")
            data = cur.fetchall()
            return render_template('Vote.html', data=data)



    else:
        flash('Already Vote this User')
        return render_template('Vote.html')


def sendmsg(targetno, message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
