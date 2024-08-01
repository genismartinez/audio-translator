import sys
import os
import openai
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
    QComboBox, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Configura tu API key de OpenAI
openai.api_key = "API-KEY"

# Lista de idiomas y sus códigos correspondientes
LANGUAGE_OPTIONS = {
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "English": "en"
    # Puedes agregar más idiomas aquí
}

# Variable global para almacenar la traducción
translated_audio_path = None


class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Audio Translator')
        self.setGeometry(100, 100, 600, 400)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout()

        self.title = QLabel('Traducir audio')
        self.title.setFont(QFont("DM Sans", 24, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: black;")
        layout.addWidget(self.title)

        self.subtitle = QLabel('Traduce cualquier audio gratis')
        self.subtitle.setFont(QFont("DM Sans", 14))
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("color: black;")
        layout.addWidget(self.subtitle)

        self.open_button = QPushButton('Abrir archivo')
        self.open_button.setFont(QFont("DM Sans", 14, QFont.Bold))
        self.open_button.setStyleSheet(
            "background-color: #007BFF; color: white;"
        )
        self.open_button.clicked.connect(self.load_audio_file)
        layout.addWidget(self.open_button)

        self.file_info_layout = QHBoxLayout()
        spacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.file_info_layout.addItem(spacer_left)

        self.file_label = QLabel('')
        self.file_label.setFont(QFont("DM Sans", 12))
        self.file_label.setStyleSheet("color: black;")
        self.file_info_layout.addWidget(self.file_label)

        self.clear_button = QPushButton('✖')
        self.clear_button.setFont(QFont("DM Sans", 12, QFont.Bold))
        self.clear_button.setStyleSheet("color: red; background-color: white; border: none;")
        self.clear_button.setVisible(False)
        self.clear_button.clicked.connect(self.clear_file)
        self.file_info_layout.addWidget(self.clear_button)

        spacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.file_info_layout.addItem(spacer_right)

        layout.addLayout(self.file_info_layout)

        self.drop_label = QLabel('o suelte el archivo aquí')
        self.drop_label.setFont(QFont("DM Sans", 12))
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setStyleSheet("color: black;")
        layout.addWidget(self.drop_label)

        self.language_label = QLabel('Target Language:')
        self.language_label.setFont(QFont("DM Sans", 12))
        self.language_label.setAlignment(Qt.AlignCenter)
        self.language_label.setStyleSheet("color: black;")
        layout.addWidget(self.language_label)

        self.language_combo = QComboBox()
        self.language_combo.setFont(QFont("DM Sans", 12))
        self.language_combo.addItems(LANGUAGE_OPTIONS.keys())
        self.language_combo.setStyleSheet("color: black;")
        self.language_combo.setFixedWidth(200)
        layout.addWidget(self.language_combo, alignment=Qt.AlignCenter)

        self.download_button = QPushButton('Descargar audio')
        self.download_button.setFont(QFont("DM Sans", 14, QFont.Bold))
        self.download_button.setStyleSheet(
            "background-color: #007BFF; color: white;"
        )
        self.download_button.setEnabled(False)
        self.download_button.clicked.connect(self.download_audio)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def load_audio_file(self, file_path=None):
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(self, 'Open Audio File', '', 'Audio Files (*.wav *.mp3)')
        if file_path:
            self.file_label.setText(f"Cargado: {os.path.basename(file_path)}")
            self.clear_button.setVisible(True)
            audio_text = self.audio_to_text(file_path)
            if audio_text:
                self.translate_audio(audio_text)

    def clear_file(self):
        self.file_label.setText('')
        self.clear_button.setVisible(False)
        self.download_button.setEnabled(False)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.wav', '.mp3')):
                self.file_label.setText(f"Cargado: {os.path.basename(file_path)}")
                self.clear_button.setVisible(True)
                self.load_audio_file(file_path)
                break

    def audio_to_text(self, audio_file_path):
        temp_wav_path = None
        try:
            if audio_file_path.lower().endswith('.mp3'):
                audio = AudioSegment.from_mp3(audio_file_path)
                temp_wav_path = audio_file_path.replace('.mp3', '.wav')
                audio.export(temp_wav_path, format='wav')
                audio_file_path = temp_wav_path

            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_file_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)

            if temp_wav_path:
                os.remove(temp_wav_path)

            return text
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to convert audio to text: {e}")
            return ""

    def translate_audio(self, audio_text):
        target_language = self.language_combo.currentText()
        translation = self.translate_text(audio_text, target_language)
        if translation:
            language_code = LANGUAGE_OPTIONS[target_language]
            self.text_to_audio(translation, language_code)

    def translate_text(self, text, target_language):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a translator."},
                    {"role": "user", "content": f"Translate the following text to {target_language}: {text}"}
                ]
            )
            translation = response.choices[0].message['content'].strip()
            return translation
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Translation failed: {e}")
            return ""

    def text_to_audio(self, text, language_code):
        global translated_audio_path
        try:
            tts = gTTS(text=text, lang=language_code)
            translated_audio_path = "translated_audio.mp3"
            tts.save(translated_audio_path)
            self.download_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save audio: {e}")

    def download_audio(self):
        global translated_audio_path
        if translated_audio_path:
            save_path, _ = QFileDialog.getSaveFileName(self, 'Save Audio File', '', 'MP3 files (*.mp3)')
            if save_path:
                os.rename(translated_audio_path, save_path)
                self.clear_file()
                QMessageBox.information(self, "Success", "Audio translated and saved successfully.")
                translated_audio_path = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator = TranslatorApp()
    translator.show()
    sys.exit(app.exec_())
