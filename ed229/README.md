# Educational Video Generator

A simple web application that creates 1-minute educational videos from any topic using AI models.

## Features

- **AI-Powered Script Generation**: Uses Mistral-7B to create educational scripts
- **Text-to-Video**: Generates video clips using damo-vilab/text-to-video-ms-1.7b
- **Text-to-Speech**: Creates voiceovers using coqui/XTTS-v2
- **Video Assembly**: Merges everything into a final video using MoviePy
- **Simple Web Interface**: Clean HTML/CSS frontend with Flask backend

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Open Your Browser**
   Navigate to `http://localhost:5000`

4. **Generate a Video**
   - Enter any educational topic (e.g., "The Water Cycle")
   - Click "Generate Video"
   - Wait for processing (may take a few minutes)
   - Download your educational video!

## How It Works

1. **Script Generation**: Mistral-7B creates a structured script with 5-6 scenes
2. **Video Creation**: Each scene description generates a 4-second video clip
3. **Audio Generation**: Narration text is converted to speech
4. **Assembly**: All clips are merged into a final 1-minute video

## System Requirements

- Python 3.8+
- 8GB+ RAM (for AI models)
- GPU recommended (for faster processing)
- 2GB+ free disk space

## Models Used

- **Script Generation**: `mistralai/Mistral-7B-Instruct-v0.2`
- **Text-to-Video**: `damo-vilab/text-to-video-ms-1.7b`
- **Text-to-Speech**: `coqui/XTTS-v2`

## Development Notes

- The app includes fallback mock implementations for development
- Models are loaded once at startup for better performance
- Temporary files are automatically cleaned up
- Check `/health` endpoint for model loading status

## Troubleshooting

- **Out of Memory**: Reduce batch sizes or use CPU-only mode
- **Model Loading Issues**: Check internet connection and Hugging Face access
- **Video Generation Fails**: Ensure MoviePy and OpenCV are properly installed

## License

This project is for educational purposes. Please respect the terms of service of the AI models used.
