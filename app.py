from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_link', methods=['POST'])
def add_link():
    url = request.form['url']
    output_lines = []

    # Call your script with the URL and capture the output
    command = ["py", "-m", "gytmdl", url]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for line in process.stdout:
        output_lines.append(line.strip())

    return jsonify({'output': output_lines})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
