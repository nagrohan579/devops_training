from flask import Flask, request
import logging

app = Flask(__name__)

# Set up logging to a file
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s')

@app.route('/')
def hello():
    logging.info('Home page accessed')
    return "Hello from Flask!"

@app.route('/ping')
def ping():
    logging.info('Ping endpoint hit from %s', request.remote_addr)
    return "Pong!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
