from flask import Flask, request
import pyrebase


config = {
    'apiKey': "AIzaSyA50ZEbRRKLiy_qwa_vE462-J-_h2CT64k",
    'authDomain': "smart-bin-da279.firebaseapp.com",
    'databaseURL': "https://smart-bin-da279.firebaseio.com",
    'projectId': "smart-bin-da279",
    'storageBucket': "smart-bin-da279.appspot.com",
    'messagingSenderId': "265397120155",
    'appId': "1:265397120155:web:ec24ff87b20c9e5ec4aa3e",
    'measurementId': "G-VNW13T1RSQ"}

import pyrebase
fire_base = pyrebase.initialize_app(config)
auth = fire_base.auth()
database = fire_base.database()
def update_fire_base(bin_id, **new_data):
    rx = database.child("bins").child(bin_id).set(new_data)
    print(rx)

def get_bin_info(in_id):
    bin = database.child("bins").child(bin_id).get().val()
    return dict(bins)

def get_bins_info():
    bins = database.child("bins").get().val()
    return dict(bins)

def locate_bin(lat, lon):
    location = "lat: {}, lng: {}".format(lat, lon)
    with open ("/home/amazing-linux/Desktop/sam-smartbin/server/home.html") as page:
        content = page.read().replace("longlat", location)
    return content

app = Flask(__name__)

@app.route("/location",  methods=['GET'])
def location():
    gps = request.args.get('gps')
    gps = gps.split(",")
    map = locate_bin(gps[0],gps[1])
    return map



@app.route("/")
def home():
    bins = []
    maps = []
    all = get_bins_info()
    for key, val in all.items():
        bins.append(str(key)+":"+val["name"])
        maps.append(val["gps"])
        content = ""
    for bin in bins:
        content = content + "<br>" + """<a href="http://127.0.0.1:5000/location?gps={}">""".format(maps[bins.index(bin)]) + bin + "</a>" + "\n"
    html = """
    <!DOCTYPE html>
    <html>
    <body>
    {}
    </body>
    </html> """.format(content)
    return html
    #return locate_bin(6.512011, 3.384875)
   


@app.route("/level", methods=['POST'])
def update_level():
    # Fetch the message
    level = request.args.get('level')
    bin_id = request.args.get('bin_id')
    gps = request.args.get('gps')
    print("recived:", level, gps, "from", bin_id)
    update_fire_base(bin_id, level=int(level), gps=gps)
    reply = "received!!!"
    return str(reply)


app.run(debug=True)
#print(get_bins_info())

# #######################################################################################################

