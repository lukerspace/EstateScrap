import scrap,datetime,json
from flask import *

# api路由
appsearch = Blueprint('appsearch',  __name__)

# 建立api 路由並且接收前端query string的要求字串並返回API所需反饋之格式
@appsearch.route("/res")
def res():
    df=scrap.get_data()
    dist = request.args.get('dist')
    floor = request.args.get('floor')
    building = request.args.get('building')
    print(dist,floor,building)
    
    con1=df["district"]==str(dist)
    con2=df["total floor number"]==int(floor)
    con3=df["building state"]==str(building)

    df["date"]=df["date"].dt.strftime('%Y-%m-%d')
    result=df.loc[con1&con2&con3]
    result = result.apply(lambda x: x.to_json(force_ascii=False), axis=1)
    data=[]
    for value in result:
        data.append(value)
    res={"data":data}

    return jsonify(res)