from sympy import subsets
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time,zipfile,os,cn2an
import pandas as pd 


valid=os.path.exists(os.path.join(os.getcwd(), 'data', 'A_lvr_land_A.csv'))
# 1. 透過爬蟲動態索取相關資料
if valid == False:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    time.sleep(5)
    driver.get("https://plvr.land.moi.gov.tw/DownloadOpenData") 
    time.sleep(3)
    driver.find_element(By.ID, 'ui-id-2').click()
    time.sleep(3)
    select = Select(driver.find_element(By.ID, 'historySeason_id'))
    select.select_by_value('108S2')
    time.sleep(3)
    select = Select(driver.find_element(By.ID, 'fileFormatId'))
    select.select_by_value('csv')
    time.sleep(3)
    driver.find_element(By.ID, 'downloadTypeId2').click()
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="table5"]/tbody/tr[7]/td[2]/input').click()
    driver.find_element(By.XPATH, '//*[@id="table5"]/tbody/tr[8]/td[2]/input').click()
    driver.find_element(By.XPATH, '//*[@id="table5"]/tbody/tr[9]/td[2]/input').click()
    driver.find_element(By.XPATH, '//*[@id="table5"]/tbody/tr[13]/td[2]/input').click()
    driver.find_element(By.XPATH, '//*[@id="table5"]/tbody/tr[20]/td[2]/input').click()
    driver.find_element(By.ID, 'downloadBtnId').click()
    print("Downloading...")
    time.sleep(40)
    print("Complete")

    with zipfile.ZipFile("/Users/hsieh/Downloads/download.zip","r") as data_zip:
        (data_zip.extractall("data"))
        print(data_zip.namelist())
else:
    pass
# 2. 創建FOLDER在工作欄位並且透彙整資料，以利API串接，匯入db操作 (本次直接採用DataFrame建立api)
def get_data():
    col=["The villages and towns urban district","transaction year month and day",\
        "building state","total floor number","main use"]
    col2=["city","date","district","building state","main use","total floor number"]

    # taipei
    df_tp=pd.read_csv("data/A_lvr_land_A.csv",skiprows=1)[col]
    df_tp=df_tp.rename(columns={"The villages and towns urban district":"district","transaction year month and day":"date"})
    df_tp["city"]="台北市"
    df_tp=(df_tp[col2])

    # new taipei
    df_ntp=pd.read_csv("data/F_lvr_land_A.csv",skiprows=1)[col]
    df_ntp=df_ntp.rename(columns={"The villages and towns urban district":"district","transaction year month and day":"date"})
    df_ntp["city"]="新北市"
    df_ntp=(df_ntp[col2])

    # taoyuan
    df_ty=pd.read_csv("data/H_lvr_land_A.csv",skiprows=1)[col]
    df_ty=df_ty.rename(columns={"The villages and towns urban district":"district","transaction year month and day":"date"})
    df_ty["city"]="桃園市"
    df_ty=(df_ty[col2])

    # taichung
    df_tc=pd.read_csv("data/B_lvr_land_A.csv",skiprows=1)[col]
    df_tc=df_tc.rename(columns={"The villages and towns urban district":"district","transaction year month and day":"date"})
    df_tc["city"]="台中市"
    df_tc=(df_tc[col2])

    #kaohsiung
    df_ks=pd.read_csv("data/E_lvr_land_A.csv",skiprows=1)[col]
    df_ks=df_ks.rename(columns={"The villages and towns urban district":"district","transaction year month and day":"date"})
    df_ks["city"]="高雄市"
    df_ks=(df_ks[col2])

    # resource
    df=pd.concat([df_tp,df_ntp,df_ty,df_tc,df_ks],axis=0).reset_index(drop=True)
    
    # set up floor info
    df["total floor number"]=df["total floor number"].str.replace("層","")
    df["total floor number"].loc[df["total floor number"].isnull()]="零"
    df["total floor number"]=df["total floor number"].apply(lambda x : cn2an.cn2an(x,"smart"))
    df["total floor number"]=df["total floor number"].astype(int)

    # set up date info 
    df["date"]=df["date"]+19110000
    df["date"]=pd.to_datetime(df['date'], format='%Y%m%d')
    df=df.sort_values(by=["date"],ascending=True)
    df.to_csv("data/data.csv")
    return df


