🖥️ Windows Setup Guide
Follow these steps to run the Python-based Image Text Extractor and Summarizer on a Windows system:

✅ **Step 1: Install Python**
  Download Python from the official site: https://www.python.org/downloads/
  During installation, check the box that says: Add Python to PATH.
  After installation, verify it:
  python --version

✅ **Step 2: Install Tesseract OCR**
  Download the Tesseract OCR installer for Windows:
  https://github.com/tesseract-ocr/tesseract/wiki
  Install it in the default location:
    C:\Program Files\Tesseract-OCR\tesseract.exe
  In your Python code (if needed), set the path:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

✅ **Step 3: Install Required Python Packages**
  Make sure pip is available:
  python -m ensurepip --upgrade
  Then install the dependencies:
  pip install pillow pytesseract nltk

✅ **Step 4: Download NLTK Data (First Time Only)**
  You need to download the tokenizer and stopwords once:
  import nltk
  nltk.download('punkt')
  nltk.download('stopwords')
  Tip: You can also run this in a Python shell or add it temporarily at the top of your script.

✅ **Step 5: Run the App**
  Run your script like this:
  python main.py
  Replace main.py with the actual file name if different.

🧾 **Summary of pip Requirements**
  Your requirements.txt should include:
  pillow
  pytesseract
  nltk

  
