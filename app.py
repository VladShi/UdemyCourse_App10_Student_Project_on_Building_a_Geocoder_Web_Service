from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import pandas as pd
from geopy.geocoders import ArcGIS

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def success():
    global ufile
    global df
    if request.method == 'POST':
        ufile = request.files['file']
        if ufile.filename.lower().endswith('.csv'):
            df = pd.read_csv(ufile, encoding = "ISO-8859-1")
            if 'Address' in df.columns or 'address' in df.columns:
                if 'address' in df.columns and 'Address' not in df.columns:
                    address = 'address'
                else:
                    address = 'Address'
                df['Latitude'] = df[address].apply(ArcGIS().geocode).apply(
                    lambda x: x.latitude if x != None else None)
                df['Longitude'] = df[address].apply(ArcGIS().geocode).apply(
                    lambda x: x.longitude if x != None else None)
                return render_template("index.html",
                                    tables=[
                                        df.to_html(classes='data',
                                                    index=False,
                                                    header="true")
                                    ],
                                    btn="download.html")
            else:
                return render_template("index.html", wrong_file="wrong_file.html")
        else:
            return render_template("index.html", wrong_file="wrong_file.html")

@app.route('/download')
def download():
    df.to_csv(secure_filename("uploaded_" + ufile.filename), index=False)
    return send_file("uploaded_" + ufile.filename, attachment_filename="yourfile.csv", as_attachment=True)

if __name__ == "__main__":
    app.debug = True
    app.run(port=5001)
