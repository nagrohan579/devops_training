from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to my simple web app!'

@app.route('/how-are-you')
def how_are_you():
    return "I'm good! How are you?"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)