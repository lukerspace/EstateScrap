import json
from pyspark.sql import SparkSession
from pyspark.sql import functions as func
from pyspark.sql.functions import to_json,col

# 透過spark索取初始csv資料
spark=SparkSession.builder.appName("project").getOrCreate()

path="data/data.csv"
# 透過基礎篩選完成條件審核
df = spark.read.option("header", "true").csv(path)
df=df.filter((df["main use"] == '住家用')).filter(df["building state"]=='住宅大樓(11層含以上有電梯)').filter(df["total floor number"]>=13)
df.show()

# 透過groupby等操作完成JSON檔案格式需求

df=df.select("city","date","district","main use")

df2=df.groupBy("city","date").agg(func.to_json\
    (func.collect_list\
        (func.create_map("district","main use")))\
            .alias("event"))

df3=df2.groupby("city").agg(func.to_json\
    (func.collect_list\
        (func.create_map("date","event")))\
            .alias("time slot"))

result1=df3.filter(df3["city"].isin(["台北市","新北市","桃園市"]))
result2=df3.filter(df3["city"].isin(["台中市","高雄市"]))


format1=[row.asDict(recursive=True) for row in result1.collect()]
format2=[row.asDict(recursive=True) for row in result2.collect()]

# 匯出資料
with open('result-part-1.json', 'w', encoding='utf-8') as file:
    json.dump(format1, file, ensure_ascii=False, indent=4)

with open('result-part-2.json', 'w', encoding='utf-8') as file:
    json.dump(format2, file, ensure_ascii=False, indent=4)