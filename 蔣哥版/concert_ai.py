import requests
from openai import OpenAI
import json
import pymysql
import pprint
from datetime import datetime

# 初始化OpenAI客戶端
client = OpenAI()
current_time = '現在時間' + datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 獲取當前時間並格式化為字符串

message = """請用繁體中文回答 詢問 
            縣市、鄉鎮市區、機構類別、醫事機構代碼、合約醫療院所名稱、接種時間、聯絡電話、地址、公費疫苗、自費疫苗
            詢問回答 縣市、鄉鎮市區、機構類別、醫事機構代碼、合約醫療院所名稱、接種時間、聯絡電話、地址、公費疫苗、自費疫苗  
            詢問死亡率 顯示疾病類型 死亡原因 詢問疫苗種類 顯示 建議疫苗種類、年齡、建議、接種劑次離開輸入= 再見
            """

# 指定要下載的CSV文件URL
urls = [
    "https://od.cdc.gov.tw/acute/Adult%20Immunization%20Schedule.csv",
    "https://od.cdc.gov.tw/acute/Vaccination%20Locations_20200803.csv",
    "https://data.tycg.gov.tw/opendata/datalist/datasetMeta/download?id=40392504-0433-4e3f-a2d0-94ee8db2a326&rid=ebd8fb00-1f61-4e76-b90f-823176b38cfd"
]

# 指定輸出的文件路徑
output_file = 'data.txt'

# 下載並寫入文件的函數
def download_and_write(urls, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for url in urls:
            try:
                response = requests.get(url, verify=False)  # 禁用證書驗證
                response.raise_for_status()  # 檢查請求是否成功
                content = response.content.decode('utf-8')  # 假設CSV文件使用UTF-8編碼
                file.write(content + '\n')  # 將內容寫入文件，並在每個文件之間添加換行符
                print(f'Successfully downloaded and wrote content from {url}')
            except requests.exceptions.RequestException as e:
                print(f'Failed to download content from {url}. Error: {e}')

# 下載CSV文件並寫入data.txt
download_and_write(urls, output_file)

# OpenAI聊天函數
def aichat():
    txt = ""
    # 指定文件路徑
    file_path = 'data.txt'

    # 開啟文件
    with open(file_path, 'r', encoding='utf-8') as file:
        # 讀取文件部分內容（限制行數）
        lines = file.readlines()[:100]  # 只讀取前100行

    # 打印文件內容
    content = ''.join(lines)
    print(content)
    txt = content

    user = input(f'請輸入問題: ')
    messages = [
        {"role": "system", "content": message},
        {"role": "assistant", "content": txt},
        {"role": "user", "content": user}
    ]

    # 確保消息總數不超過模型的最大限制
    while sum(len(m["content"]) for m in messages) > 16000:
        messages.pop(1)  # 移除最早的assistant消息

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    response_message = completion.choices[0].message
    result = response_message.content
    print(result)

    return result

# 執行聊天函數
aichat()
