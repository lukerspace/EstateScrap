from flask import *
from api_search import appsearch

# 建立FLASK框架測試api返回情況
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"] = False

app.register_blueprint(appsearch, url_prefix='/api')

@app.route('/')
def index():
	return render_template("index.html")

app.run(port=3000)