import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw
import pytesseract
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict

# Download NLTK data (only required once)
import nltk
nltk.download('punkt')
nltk.download('stopwords')

# Set the path to the Tesseract executable (if needed)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Custom colors and fonts
BG_COLOR = "#211951"  # Dark background
PATTERN_COLOR = "#1D1616"  # Dark gray pattern
BUTTON_COLOR = "#15F5BA"  # Dark red button color
BUTTON_HOVER_COLOR = "#836FFF"  # Light red hover color
BUTTON_TEXT_COLOR = "#000000"  # Black text color
TEXT_COLOR = "#15F5BA"
TEXT_BOX_COLOR_FONT_COLOR = "#ffffff"
BUTTON_OUTLINE_COLOR = "#15F5BA"  # Gray outline color
TEXT_BOX_COLOR = "#1D1616"  # Dark gray for text boxes
FONT = ("Helvetica", 12)
BUTTON_FONT = ("Helvetica", 11, "bold")


def extract_text_from_image(image_path):
    """
    Extracts text from an image using pytesseract.
    """
    try:
        image = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text
    except Exception as e:
        messagebox.showerror("Error", f"Failed to extract text: {e}")
        return ""

def summarize_text(text, summary_length=3):
    """
    Summarizes the extracted text using NLTK.
    """
    try:
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)
        
        # Tokenize the text into words
        words = word_tokenize(text.lower())
        
        # Remove stopwords
        stop_words = set(stopwords.words("english"))
        words = [word for word in words if word.isalnum() and word not in stop_words]
        
        # Calculate word frequency
        word_frequencies = defaultdict(int)
        for word in words:
            word_frequencies[word] += 1
        
        # Score sentences based on word frequency
        sentence_scores = defaultdict(int)
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in word_frequencies:
                    sentence_scores[sentence] += word_frequencies[word]
        
        # Get the top N sentences with the highest scores
        summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:summary_length]
        summary = " ".join(summarized_sentences)
        return summary
    except Exception as e:
        messagebox.showerror("Error", f"Failed to summarize text: {e}")
        return ""

def open_image():
    """
    Opens an image file, extracts text, and summarizes it.
    """
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff;*.tif")]
    )
    
    if file_path:
        try:
            # Display the selected image in the left section
            image = Image.open(file_path)
            image.thumbnail((400, 500))  # Resize the image to fit in the UI
            photo = ImageTk.PhotoImage(image)
            image_label.config(image=photo)
            image_label.image = photo  # Keep a reference to avoid garbage collection

            # Extract text from the image
            extracted_text = extract_text_from_image(file_path)
            text_box.delete(1.0, tk.END)  # Clear previous text
            text_box.insert(tk.END, extracted_text)  # Insert extracted text

            # Summarize the extracted text
            summary = summarize_text(extracted_text)
            summary_box.delete(1.0, tk.END)  # Clear previous summary
            summary_box.insert(tk.END, summary)  # Insert summary

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main application window
root = tk.Tk()
root.title("Image Text Extractor and Summarizer")
root.geometry("1200x600")  # Set window size
root.configure(bg=BG_COLOR)  # Set background color

# Create a dark gray pattern for the background
pattern = Image.new("RGB", (20, 20), PATTERN_COLOR)
draw = ImageDraw.Draw(pattern)
draw.rectangle([0, 0, 10, 10], fill=PATTERN_COLOR)
draw.rectangle([10, 10, 20, 20], fill=PATTERN_COLOR)
pattern = ImageTk.PhotoImage(pattern)

background_label = tk.Label(root, image=pattern)
background_label.place(relwidth=1, relheight=1)

# Create a left frame for the image and button (40% of the window)
left_frame = tk.Frame(root, bg=BG_COLOR)
left_frame.place(relx=0, rely=0, relwidth=0.4, relheight=1)

# Create a button to open an image
open_button = tk.Button(
    left_frame,
    text="SELECT IMAGE",
    font=BUTTON_FONT,
    bg=BUTTON_COLOR,
    fg=BUTTON_TEXT_COLOR,
    activebackground=BUTTON_HOVER_COLOR,
    activeforeground=BUTTON_TEXT_COLOR,
    relief="solid",
    bd=2,
    highlightbackground=BUTTON_OUTLINE_COLOR,
    command=open_image
)
open_button.pack(pady=20)

# Create a label to display the selected image
image_label = tk.Label(left_frame, bg=BG_COLOR)
image_label.pack()

# Create a right frame for the text and summary (60% of the window)
right_frame = tk.Frame(root, bg=BG_COLOR)
right_frame.place(relx=0.4, rely=0, relwidth=0.6, relheight=1)

# Create a text box to display the extracted text (60% of the right section)
text_label = tk.Label(right_frame, text="EXTRACTED TEXT", font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
text_label.pack(pady=(10, 0))

text_frame = tk.Frame(right_frame, bg=BG_COLOR)
text_frame.pack(fill=tk.BOTH, expand=True, pady=10)

text_box = tk.Text(text_frame, wrap=tk.WORD, height=15, font=FONT, bg=TEXT_BOX_COLOR, fg=TEXT_BOX_COLOR_FONT_COLOR)
text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True,padx=20)

# Add a scrollbar to the text box
scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_box.config(yscrollcommand=scrollbar.set, highlightbackground=BUTTON_OUTLINE_COLOR,highlightthickness=1, relief="solid", bd=0)

# Create a text box to display the summary (40% of the right section)
summary_label = tk.Label(right_frame, text="SUMMARY", font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
summary_label.pack(pady=(10, 0))

summary_box = tk.Text(right_frame, wrap=tk.WORD, height=15, font=FONT, bg=TEXT_BOX_COLOR, fg=TEXT_BOX_COLOR_FONT_COLOR)
summary_box.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Add rounded corners to the summary box
summary_box.config(highlightbackground=BUTTON_OUTLINE_COLOR, highlightthickness=1, relief="solid", bd=0)

# Run the Tkinter event loop
root.mainloop()