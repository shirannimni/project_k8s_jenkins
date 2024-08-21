from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    current_time = datetime.now().strftime("%H:%M:%S")
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Current Time</title>
        <style>
            body {
                background-color: blue;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                font-family: Arial, sans-serif;
                font-size: 2em;
            }
        </style>
    </head>
    <body>
        <div>Current Time: {{ time }}</div>
    </body>
    </html>
    '''
    return render_template_string(html, time=current_time)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
