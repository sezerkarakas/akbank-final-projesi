from flask import Flask, request, jsonify, render_template
from chatbot import generateAnswer, initialize_rag_system
from chat_with_pandasai import initialize_pandasai_system, generatePandasAIAnswer, update_pandasai_system
import markdown2
import os
from io import BytesIO
import base64

app = Flask(__name__)

initialize_rag_system()
initialize_pandasai_system()

DATA_KEYWORDS = ['veri', 'csv', 'tablo', 'grafik', 'veri seti', 'pandas']

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/get', methods=['POST'])
def get_bot_response():
    user_message = request.form['msg']
    if any(keyword in user_message.lower() for keyword in DATA_KEYWORDS) and os.path.exists("pandasai_data/kullanici_data.csv"):
        response = generatePandasAIAnswer(user_message)
        if response.endswith(".png"):
            image_path = response
            return jsonify({'text': html_response, 'image': image_path})
    else:
        response = generateAnswer(user_message)
    html_response = markdown2.markdown(response)
    return jsonify({'text': html_response})

@app.route('/delete', methods=["POST"])
def delete_file():
    os.remove("pandasai_data/kullanici_data.csv")
    return "File deleted successfully."

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.csv'):
        filepath = "pandasai_data/kullanici_data.csv"
        file.save(filepath)
        # Update the PandasAI system with the new data
        update_pandasai_system(filepath)
        return 'File uploaded and processed successfully'
    return 'Invalid file type. Only CSV files are allowed.'

if __name__ == '__main__':
    app.run(debug=True)