import os
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

FILES_DIR = "files"

def extract_text_from_pdf(pdf_path):
    """
    Tenta extrair texto de um PDF.
    1) PyMuPDF para PDFs textuais.
    2) OCR com Tesseract se o PDF for escaneado.
    Retorna um dicionário com texto e método usado.
    """
    # Tentativa 1: PyMuPDF (texto digital)
    try:
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        if text.strip():
            return {"method": "PyMuPDF", "text": text}
    except Exception:
        pass

    # Tentativa 2: OCR com pytesseract
    try:
        images = convert_from_path(pdf_path)
        ocr_text = ""
        for img in images:
            ocr_text += pytesseract.image_to_string(img, lang="por")
        if ocr_text.strip():
            return {"method": "Tesseract OCR", "text": ocr_text}
    except Exception as e:
        return {"method": "Erro", "text": f"Erro ao processar {pdf_path}: {str(e)}"}

    # Futuro: fallback Amazon Textract pode ser chamado aqui

    return {"method": "Desconhecido", "text": ""}


def main():
    files = [f for f in os.listdir(FILES_DIR) if f.lower().endswith(".pdf")]

    if not files:
        print("Nenhum PDF encontrado na pasta 'files'.")
        return

    for file in files:
        path = os.path.join(FILES_DIR, file)
        result = extract_text_from_pdf(path)
        method = result["method"]
        text = result["text"]

        print(f"\n=== PDF: {file} ===")
        print(f"== Método de extração: {method} ==")
        print(text[:1000])  # mostra apenas os primeiros 1000 caracteres no console
        print("=" * 80)


if __name__ == "__main__":
    main()
