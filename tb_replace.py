from flask import Flask, render_template, request, send_file, jsonify
import os
import pandas as pd
import re

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
TERMINOLOGY_FOLDER = 'terminology_files'

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# List of products and corresponding terminology files
PRODUCTS = {
    "HCI": "HCI_Terminology.xlsx",
    "NSF": "NSF_Terminology.xlsx",
    "CC": "CC_Terminology.xlsx",
    "IAG": "IAG_Terminology.xlsx",
    "SCP": "SCP_Terminology.xlsx",
    "VDI": "VDI_Terminology.xlsx",
    "aTrust": "aTrust_Terminology.xlsx",
    "ES": "ES_Terminology.xlsx",
    "SKE": "SKE_Terminology.xlsx"
}

def load_terminology(product):
    terminology_file = os.path.join(TERMINOLOGY_FOLDER, PRODUCTS[product])
    if not os.path.exists(terminology_file):
        return None

    terminology = pd.read_excel(terminology_file)
    return dict(zip(terminology.iloc[:, 0].astype(str), terminology.iloc[:, 1].astype(str)))

def replace_terminology_text(text, terminology_dict):
    if not text or not terminology_dict:
        return text
    
    sorted_terms = sorted(terminology_dict.keys(), key=len, reverse=True)
    
    for term in sorted_terms:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        text = pattern.sub(lambda match: terminology_dict[term], text)
        
    return text

def replace_terminology_text_reverse(text, terminology_dict):
    if not text or not terminology_dict:
        return text
    
    reverse_dict = {v: k for k, v in terminology_dict.items()}
    sorted_terms = sorted(reverse_dict.keys(), key=len, reverse=True)
    
    for term in sorted_terms:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        text = pattern.sub(lambda match: reverse_dict[term], text)
        
    return text


def replace_terminology_file(file_a, file_b, output_file):
    terminology_dict = load_terminology(file_a)
    if terminology_dict is None:
        return None

    file_b_data = pd.read_excel(file_b)
    updated_data = file_b_data.applymap(lambda x: replace_terminology_text(str(x), terminology_dict) if pd.notna(x) else x)
    
    updated_data.to_excel(output_file, index=False, engine='openpyxl')
    return output_file

@app.route('/')
def index():
    return render_template('index.html', products=PRODUCTS.keys())

@app.route('/upload', methods=['POST'])
def upload():
    product = request.form.get('product')
    file_b = request.files.get('file_b')

    if not product or not file_b:
        return "Product and file must be selected.", 400

    terminology_dict = load_terminology(product)
    if terminology_dict is None:
        return f"Terminology file for {product} not found.", 400

    file_b_path = os.path.join(UPLOAD_FOLDER, file_b.filename)
    file_b.save(file_b_path)

    output_file = os.path.join(OUTPUT_FOLDER, f"replaced_{file_b.filename}")
    result_file = replace_terminology_file(product, file_b_path, output_file)

    if not result_file:
        return "Error processing file.", 500

    return send_file(result_file, as_attachment=True)

@app.route('/replace_text', methods=['POST'])
def replace_text():
    product = request.json.get('product')
    input_text = request.json.get('input_text')
    direction = request.json.get('direction', 'zh_to_en')

    if not product or not input_text:
        return jsonify({"error": "Product and text must be provided"}), 400

    terminology_dict = load_terminology(product)
    if terminology_dict is None:
        return jsonify({"error": f"Terminology file for {product} not found"}), 400

    if direction == 'zh_to_en':
        replaced_text = replace_terminology_text(input_text, terminology_dict)
    else:
        replaced_text = replace_terminology_text_reverse(input_text, terminology_dict)
    
    return jsonify({"replaced_text": replaced_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
