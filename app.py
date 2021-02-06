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
    if request.method == 'POST':
        ufile = request.files['file']
        # ufile.save(secure_filename("uploaded_" + ufile.filename))
        df = pd.read_csv(ufile)
        if 'Address' in df.columns or 'address' in df.columns:
            if 'address' in df.columns and 'Address' not in df.columns:
                address = 'address'
            else:
                address = 'Address'
            df['Latitude'] = df[address].apply(ArcGIS().geocode).apply(lambda x: x.latitude if x != None else None) 
            df['Longitude'] = df[address].apply(ArcGIS().geocode).apply(lambda x: x.longitude if x != None else None)
            return render_template("index.html", btn="download.html")
        else:
            pass  # notification about file has not "address" column 

if __name__ == "__main__":
    app.debug=True
    app.run(port=5001)
