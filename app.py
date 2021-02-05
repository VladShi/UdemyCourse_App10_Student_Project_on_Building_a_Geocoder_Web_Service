from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/success')
def success():
    pass

if __name__ == "__main__":
    app.debug=True
    app.run(port=5001)
