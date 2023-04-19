from flask import Flask, render_template, request, send_file
from ai import custom_img

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/call', methods=['POST'])
def handle_data():
    data = request.get_json()
    photo1 = data['photo1']
    photo2 = data['photo2']
    custom_img(photo1, photo2)
    print("It's done!")
    return 'Data received'

@app.route('/<path:url>')
def send_image(url):
    return send_file(url, mimetype='image/png')

if __name__ == '__main__':
    app.run()