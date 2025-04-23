from flask import Flask, render_template, redirect
from tinyDB import ProjectBinDatabase 
import time
import qrcode

app = Flask(__name__)
db = ProjectBinDatabase("/home/ciara/Documents/FinalYrPro/db.json") 


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/data')
def index():
    data = db.get_all_detections()  
    return render_template('index.html', data=data)  

@app.route('/live')
def live():
    return redirect("http://172.20.10.7:4912/")

@app.template_filter('datetimeformat')
def datetimeformat(value):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(value))

def make_qr_code():
    url = "https://github.com/CiaraC03/FinalYrProject"
    img = qrcode.make(url)
    img.save("/home/ciara/Documents/FinalYrPro/static/qrCode.png")


def run_flask():
    make_qr_code()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
