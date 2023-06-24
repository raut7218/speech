import pytesseract
from PIL import Image
import gtts
import webbrowser
import datetime
import streamlit as st
import cv2
import numpy as np

# Path to the Tesseract executable (change it if necessary)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Function to extract text from an image
def extract_text_from_image(image_path, language):
    # Open the image file
    image = Image.open(image_path)

    # Convert the image to grayscale
    image = image.convert("L")

    # Use Tesseract to extract text from the image
    text = pytesseract.image_to_string(image, lang=language)

    return text

# function to translate the text from source to destination language using open source googletrans library
def translate_text(text, dest_language):
    from googletrans import Translator
    translator = Translator()
    translated = translator.translate(text, dest=dest_language)
    return translated.text

# Function to convert text to speech using Google Text-to-Speech
def convert_text_to_speech(text, language):
    # Convert the text to speech using Google Text-to-Speech
    speech = gtts.gTTS(text, lang=language)

    # Get the current time
    now = datetime.datetime.now()

    # Save the speech file with a name that includes the current time
    output_file = f"speech_{now.strftime('%Y-%m-%d_%H-%M-%S')}.mp3"
    speech.save(output_file)

    # Open the sound file in the default music player
    #webbrowser.open(output_file)
    st.audio(output_file)

#upload file using streamlit
uploaded_file = st.file_uploader("Upload an image...", type="")

# dropdown for language selection from image to text conversion
languages = {
    '': '',  # Empty option
    'English': 'eng',
    'Marathi': 'mar',
    'Hindi': 'hin',
    'Panjabi': 'pan'
}
selected_language = st.selectbox('Select a language', list(languages.keys()))
language_code = languages[selected_language]  # Get the selected language code
st.write('Language code:', language_code)

# dropdown for language selection from text to speech conversion
languages_ = {
    '': '',  # Empty option
    'English': 'en',
    'Marathi': 'mr',
    'Hindi': 'hi',
    'Panjabi': 'pa'
}
selected_language_ = st.selectbox('Select a language for translation', list(languages_.keys()))
language_code_ = languages_[selected_language_]  # Get the selected language code
st.write('Language code:', language_code_)

# Check if the file is uploaded and language selected is not empty
if uploaded_file is not None and language_code != '' and language_code_ != '':
    # Convert the file to an opencv image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    # Display the image
    st.image(image, channels="BGR")

    # Save the image to disk
    cv2.imwrite("uploaded_image.jpg", image)

    # Get the extracted text
    text = extract_text_from_image("uploaded_image.jpg", language_code)

    # Display the extracted text
    st.write(text)

    # Get the translated text
    translated_text = translate_text(text, language_code_)

    # Display the translated text
    st.write(translated_text)

    # Convert the text to speech
    convert_text_to_speech(translated_text, language=language_code_)
