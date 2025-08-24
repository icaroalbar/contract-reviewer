import os
import json
import boto3
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from io import BytesIO

# Configurações
S3_INPUT_BUCKET = os.environ.get("S3_BUCKET")  # bucket de entrada
S3_OUTPUT_BUCKET = "my-textract-output"        # bucket de saída
s3_client = boto3.client("s3")

def download_pdf_from_s3(key):
    """Baixa o PDF da S3 para memória"""
    obj = s3_client.get_object(Bucket=S3_INPUT_BUCKET, Key=key)
    return BytesIO(obj['Body'].read())

def extract_text_from_pdf(file_like):
    """Tenta extrair texto do PDF, ou usa OCR local"""
    try:
        text = ""
        doc = fitz.open(stream=file_like, filetype="pdf")
        for page in doc:
            text += page.get_text()
        if text.strip():
            return text
    except Exception:
        pass

    # Se não extraiu texto, faz OCR
    try:
        file_like.seek(0)
        images = convert_from_path(file_like)
        ocr_text = ""
        for img in images:
            ocr_text += pytesseract.image_to_string(img, lang="por")
        return ocr_text
    except Exception as e:
        return f"Erro ao processar PDF: {str(e)}"

def save_text_to_s3(pdf_key, text):
    """Salva o texto extraído em formato JSON na bucket de saída"""
    json_key = f"{os.path.splitext(pdf_key)[0]}.json"
    s3_client.put_object(
        Bucket=S3_OUTPUT_BUCKET,
        Key=json_key,
        Body=json.dumps({"pdf": pdf_key, "text": text}),
        ContentType="application/json"
    )
    return json_key

def lambda_handler(event, context):
    """Função Lambda principal"""
    # Lista arquivos PDF na bucket de entrada
    response = s3_client.list_objects_v2(Bucket=S3_INPUT_BUCKET)
    pdf_keys = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].lower().endswith(".pdf")]

    if not pdf_keys:
        return {"statusCode": 200, "body": {"message": "Nenhum PDF encontrado na S3."}}

    results = {}
    for key in pdf_keys:
        pdf_file = download_pdf_from_s3(key)
        text = extract_text_from_pdf(pdf_file)
        json_key = save_text_to_s3(key, text)  # salva todo o texto
        results[key] = {"s3_json_key": json_key}

    return {"statusCode": 200, "body": results}
