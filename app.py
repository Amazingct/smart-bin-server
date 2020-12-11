from flask import Flask, request
import pyrebase


config = {
    "apiKey": "AIzaSyAGvaBLvQAjJAMBLgZkRPYtkhBbgYnqaPU",
    "authDomain": "finalbin-35e3c.firebaseapp.com",
    "databaseURL": "https://finalbin-35e3c-default-rtdb.firebaseio.com",
    "projectId": "finalbin-35e3c",
    "storageBucket": "finalbin-35e3c.appspot.com",
    "messagingSenderId": "887888512503",
    "appId": "1:887888512503:web:b987d613ed083aee569af2",
    "measurementId": "G-GX8J1JVNC5"}

import pyrebase
fire_base = pyrebase.initialize_app(config)
auth = fire_base.auth()
database = fire_base.database()
def get_bin_info(in_id):
    bin = database.child("bins").child(bin_id).get().val()
    return dict(bins)

def get_bins_info():
    bins = database.child("bins").get().val()
    return dict(bins)

def locate_bin(lat, lon, level):
    location = "lat: {}, lng: {}".format(lat, lon)
    with open ("mapping.html") as page:
        content = page.read().replace("blat", lat)
        content = content.replace("blng", lon)
        content = content.replace("level", level)
        
    return content

app = Flask(__name__)

@app.route("/location",  methods=['GET'])
def location():
    gps = request.args.get('gps')
    level = request.args.get('Level')
    gps = gps.split(",")
    map = locate_bin(gps[0],gps[1], level )
    return map

@app.route("/")
def home():
    bins = []
    maps = []
    levels = []
    all = get_bins_info()
    print(all)
    for key, val in all.items():
        bins.append(str(key) + " LEVEL: " + str(val["Level"]))
        maps.append(val["gps"])
        levels.append(str(val["Level"]))
        content = ""
    for bin in bins:
        content = content + "<br>" + """<a href="https://finalbin.herokuapp.com/location?gps={}&Level={}">""".format(maps[bins.index(bin)],levels[bins.index(bin)]) + bin + "</a>" + "\n"
    html = """
    <!DOCTYPE html>
    <html>
    <body>
    {}
    </body>
    </html> """.format(content)
    return html
    #return locate_bin(6.512011, 3.384875)
   


app.run(debug=True)
#print(get_bins_info())

# #######################################################################################################

