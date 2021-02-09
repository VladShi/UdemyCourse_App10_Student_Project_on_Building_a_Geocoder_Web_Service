from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import pandas as pd
from geopy.geocoders import ArcGIS
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/success', methods=['POST'])
def success():
    global df
    if request.method == 'POST':
        ufile = request.files['file']
        try:
            df = pd.read_csv(ufile, encoding="ISO-8859-1")
            if 'address' in df.columns:
                address = 'address'
            elif 'Address' in df.columns:
                address = 'Address'
            df['Latitude'] = df[address].apply(ArcGIS().geocode).apply(
                lambda x: x.latitude if x != None else None)
            df['Longitude'] = df[address].apply(ArcGIS().geocode).apply(
                lambda x: x.longitude if x != None else None)
            return render_template("index.html",
                                   text=df.to_html(index=False),
                                   btn="download.html")
        except:
            return render_template(
                "index.html",
                text=
                "Please make sure you upload a CSV file and you have an address column in your CSV file!"
            )


@app.route('/download')
def download():
    filename = "uploads/geo_" + str(time.time()) + ".csv"
    df.to_csv(filename, index=False)
    return send_file(filename,
                     attachment_filename="yourfile.csv",
                     as_attachment=True)


if __name__ == "__main__":
    app.debug = True
    app.run(port=5001)
