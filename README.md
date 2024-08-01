# Audio Translator

Audio Translator is a Python-based application that allows users to translate audio files into different languages. The application uses OpenAI's GPT-3.5 for translation and Google's Text-to-Speech (gTTS) for converting the translated text back into audio. The user interface is built with PyQt5, providing a modern and interactive experience.

## Features

- **Drag and Drop**: Easily drag and drop audio files into the application.
- **Multiple Languages**: Supports translation into multiple languages including Spanish, French, German, and English.
- **Audio Conversion**: Converts the translated text into audio using gTTS.
- **File Management**: Allows users to load, translate, and save audio files with a user-friendly interface.
- **Clear Loaded Files**: Option to clear a loaded file and load a new one.

## Requirements

- Python 3.x
- PyQt5
- OpenAI API Key
- SpeechRecognition
- pydub
- gTTS

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/audio-translator.git
    cd audio-translator
    ```

2. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set your OpenAI API key**:

    Open the `main.py` file and set your OpenAI API key:

    ```python
    openai.api_key = 'your-api-key'
    ```

## Usage

1. **Run the application**:

    ```bash
    python main.py
    ```

2. **Using the Application**:
    - Drag and drop an audio file (MP3 or WAV) into the application window or click the "Open file" button to select a file from your file system.
    - Select the target language from the dropdown menu.
    - Click the "Translate" button to translate the audio.
    - Once the translation is complete, click the "Download audio" button to save the translated audio file.

## Detailed Description

### User Interface

The application interface is divided into several sections:

1. **Title and Subtitle**:
    - The title "Cortar audio" and subtitle "Recorta o corta cualquier archivo de audio en línea" are displayed at the top, providing a brief description of the application's purpose.

2. **Open File Button**:
    - The "Open file" button allows users to select an audio file from their file system. The button has a blue background with white, bold text.

3. **File Information**:
    - Below the "Open file" button, the name of the loaded file is displayed along with a red cross button to clear the loaded file.

4. **Drag and Drop Area**:
    - Users can also drag and drop audio files into the application window. The prompt "or drop the file here" is displayed to guide users.

5. **Language Selection**:
    - A dropdown menu labeled "Target Language" allows users to select the target language for translation.

6. **Download Button**:
    - The "Download audio" button is enabled once the translation is complete, allowing users to save the translated audio file.

### Functionality

- **Load Audio File**:
    - Users can load an audio file either by clicking the "Open file" button or by dragging and dropping the file into the application window.
    - The application supports MP3 and WAV file formats.

- **Clear Loaded File**:
    - The red cross button next to the loaded file name allows users to clear the current file and load a new one.

- **Translate Audio**:
    - After selecting a target language, users can click the "Translate" button to translate the audio. The application uses OpenAI's GPT-3.5 to translate the audio text.

- **Download Translated Audio**:
    - Once the translation is complete, the "Download audio" button is enabled. Users can click this button to save the translated audio file.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure your code adheres to the project's coding standards and includes appropriate test coverage.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenAI](https://openai.com/) for providing the translation API.
- [Google Text-to-Speech](https://pypi.org/project/gTTS/) for converting text to audio.
- [PyQt5](https://pypi.org/project/PyQt5/) for the graphical user interface.
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) for converting audio to text.
- [pydub](https://pypi.org/project/pydub/) for audio file manipulation.

