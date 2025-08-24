import os
import boto3
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from io import BytesIO

# Configurações
S3_BUCKET = os.environ.get("S3_BUCKET")
s3_client = boto3.client("s3")

def download_pdf_from_s3(key):
    """Baixa o PDF da S3 para memória"""
    obj = s3_client.get_object(Bucket=S3_BUCKET, Key=key)
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

def main():
    # Lista arquivos PDF na bucket
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
    pdf_keys = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].lower().endswith(".pdf")]

    if not pdf_keys:
        print("Nenhum PDF encontrado na S3.")
        return

    for key in pdf_keys:
        print(f"\n=== PDF: {key} ===\n")
        pdf_file = download_pdf_from_s3(key)
        text = extract_text_from_pdf(pdf_file)
        print(text[:1000])  # mostra os primeiros 1000 caracteres
        print("="*80)

if __name__ == "__main__":
    main()
