import pandas as pd
import os
from pandasai import Agent
from pandasai.llm.google_gemini import GoogleGemini
from pandasai import SmartDataframe
from dotenv import load_dotenv
load_dotenv()

csv_file_path = "pandasai_data/kullanici_data.csv"

google_api_key = os.environ["GOOGLE_API_KEY"]

prompt = """
Sen Akbank' ın dijital bir asistanısın. Amacın verilerden yararlanarak kullanıcının sorduğu soruya uygun şekilde cevap vermek.
Önemli notlar:
1. Kullanıcının sorusuna hangi dilde sorulmuşsa o dilde cevap verin. Ön tanımlı olarak Türkçe cevap ver.
2. Cevaplarınızı net, detaylı ve anlaşılır bir şekilde verin.
3. Sorular, finansal bilgiler ve kullanıcı verileriyle ilgilidir.
4. Eğer soruya cevap bulamadıysan, "Bilmiyorum." yaz.
5. Görselleştirme ile ilgili bir soru sorulursa görselleştirme yapma, sadece görseli kaydettiğin konumu yaz.
Eğer hazırsan, sana kullanıcının sorusunu sağlıyorum.
"""

llm = None
sdf = None

def initialize_pandasai_system():
    global llm, sdf
    llm = GoogleGemini(api_key=google_api_key)
    
    # DataFrame'i yükleyin veya boş bir DataFrame oluşturun
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
    else:
        df = pd.DataFrame()  # Boş DataFrame

    sdf = SmartDataframe(df=df, config={"llm": llm, 'open_charts': False})

def update_pandasai_system(filepath):
    global sdf
    df = pd.read_csv(filepath)
    sdf = SmartDataframe(df=df, config={"llm": llm, 'open_charts': False})

def generatePandasAIAnswer(query):
    query = prompt + query
    response = sdf.chat(query)
    return response

if __name__ == "__main__":
    initialize_pandasai_system()  # Sistemi başlat
    response = generatePandasAIAnswer("cinsiyere göre hayatta kalma oranını görselleştirir misin")
    for i in response:
        print(i)