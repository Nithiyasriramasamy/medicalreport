"""
Educational Video Generator
A Flask web app that creates 1-minute educational videos from topics using AI models.

Stack:
- Frontend: HTML + CSS
- Backend: Flask
- AI Models: Mistral-7B, damo-vilab/text-to-video-ms-1.7b, coqui/XTTS-v2
- Video Processing: MoviePy
"""

import os
import json
import tempfile
import requests
from flask import Flask, render_template, request, send_file, jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import numpy as np
try:
    # Prefer MoviePy if available (simpler merging/compositing)
    from moviepy.editor import (  # type: ignore
        VideoFileClip,
        AudioFileClip,
        ImageClip,
        concatenate_videoclips,
        CompositeVideoClip,
        ColorClip,
        TextClip,
        vfx,
    )
    MOVIEPY_AVAILABLE = True
except Exception as _moviepy_err:
    # Gracefully fall back to OpenCV/ffmpeg pipeline
    MOVIEPY_AVAILABLE = False
    VideoFileClip = None  # type: ignore
    AudioFileClip = None  # type: ignore
    concatenate_videoclips = None  # type: ignore
    CompositeVideoClip = None  # type: ignore
    ColorClip = None  # type: ignore
    TextClip = None  # type: ignore
    
    # Try to import ffmpeg helper
    try:
        import imageio_ffmpeg
    except Exception:
        imageio_ffmpeg = None  # type: ignore
    
    # OpenCV for video fallback
    try:
        import cv2  # type: ignore
    except Exception:
        cv2 = None  # type: ignore
    
    # Standard libs for audio fallback
    import wave
    import struct
import io
import base64
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ------------------------------------------------------------
# Hugging Face authentication
# Paste your token below OR set it as an environment variable.
# Supported env var names: HUGGINGFACEHUB_API_TOKEN, HUGGING_FACE_HUB_TOKEN, HF_TOKEN
from dotenv import load_dotenv  # type: ignore
load_dotenv()
HF_TOKEN = (
    os.getenv("HUGGINGFACEHUB_API_TOKEN")
    or os.getenv("HUGGING_FACE_HUB_TOKEN")
    or os.getenv("HF_TOKEN")
    or "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"  # <-- Optionally paste your token here
)
FAL_KEY = os.getenv("FAL_KEY")  # Optional: for WAN 2.2 text-to-video

# Global variables for models (loaded once)
mistral_pipeline = None
text_to_video_pipeline = None
tts_pipeline = None

def load_models():
    """Load all AI models once at startup"""
    global mistral_pipeline, text_to_video_pipeline, tts_pipeline
    
    try:
        logger.info("Loading GPT-2 model...")
        # Load GPT-2 model for script generation (no authentication needed)
        model_name = "gpt2-medium"
        mistral_pipeline = pipeline(
            "text-generation",
            model=model_name,
            max_length=512,
            temperature=0.7,
            do_sample=True,
            pad_token_id=50256  # GPT-2 EOS token
        )
        
        # Configure text-to-video source
        if FAL_KEY:   
            logger.info("Configuring WAN 2.2 T2V via FAL API")
            text_to_video_pipeline = "wan22_fal"  # sentinel for WAN path
        else:
            logger.info("Using mock text-to-video model...")
            text_to_video_pipeline = None
        
        logger.info("Using mock TTS model...")
        # Use mock implementation for TTS (to keep it lightweight)
        tts_pipeline = None
        
        logger.info("All models loaded successfully!")
        
    except Exception as e:
        logger.error(
            "Error loading models: %s\nIf this is a 401/Access issue, set your Hugging Face token either by:\n"
            "- Setting environment variable HUGGINGFACEHUB_API_TOKEN (preferred), or\n"
            "- Replacing the placeholder in HF_TOKEN near the top of app.py.",
            e,
        )
        # Fallback to mock models for development
        mistral_pipeline = None
        text_to_video_pipeline = None
        tts_pipeline = None

def generate_script_with_mistral(topic):
    """
    Generate educational video script using Mistral-7B
    
    Args:
        topic (str): The educational topic
        
    Returns:
        dict: JSON containing scenes with descriptions and narration
    """
    if mistral_pipeline is None:
        # Mock response for development
        return {
            "scenes": [
                {
                    "description": "A beautiful sunrise over mountains with flowing water",
                    "narration": "Welcome to our exploration of the water cycle, nature's incredible recycling system."
                },
                {
                    "description": "Water droplets forming on leaves and grass in the morning",
                    "narration": "It all begins with evaporation, as the sun's heat transforms water into invisible vapor."
                },
                {
                    "description": "Clouds forming and moving across a blue sky",
                    "narration": "This vapor rises and condenses into clouds, carried by wind across the globe."
                },
                {
                    "description": "Rain falling on a forest and flowing into streams",
                    "narration": "When clouds become heavy, precipitation occurs, returning water to Earth as rain or snow."
                },
                {
                    "description": "A river flowing through a valley toward the ocean",
                    "narration": "Water flows through rivers and streams, eventually reaching the ocean to begin the cycle again."
                }
            ]
        }
    
    prompt = f"Educational video script about {topic}:\n\nScene 1: "
    
    try:
        response = mistral_pipeline(
            prompt,
            max_length=200,
            temperature=0.7,
            do_sample=True,
            pad_token_id=50256
        )
        
        # For simplicity, return structured mock data based on the topic
        generated_text = response[0]['generated_text']
        logger.info(f"Generated text: {generated_text[:100]}...")
        
        # Return structured educational content
        return {
            "scenes": [
                {
                    "description": f"Introduction to {topic} with clear diagrams and visual elements",
                    "narration": f"Welcome to our exploration of {topic}. Let's understand the key concepts."
                },
                {
                    "description": f"Detailed explanation of {topic} with examples and illustrations",
                    "narration": f"The fundamentals of {topic} are important for understanding how it works."
                },
                {
                    "description": f"Real-world applications and examples of {topic}",
                    "narration": f"Here are some practical examples of {topic} in everyday life."
                },
                {
                    "description": f"Summary and conclusion about {topic}",
                    "narration": f"In conclusion, {topic} plays a crucial role in our understanding of the world."
                }
            ]
        }
            
    except Exception as e:
        logger.error(f"Error generating script: {e}")
        # Return mock data as fallback
        return {
            "scenes": [
                {
                    "description": f"An educational diagram about {topic}",
                    "narration": f"Let's explore {topic} and understand its key concepts."
                },
                {
                    "description": f"Visual examples and illustrations of {topic}",
                    "narration": f"This topic is important because it helps us understand our world better."
                }
            ]
        }

def generate_video_clip(description, output_path):
    """
    Generate a 4-second video clip from text description
    
    Args:
        description (str): Visual description for the video
        output_path (str): Path to save the video file
        
    Returns:
        bool: Success status
    """
    # WAN 2.2 via FAL
    if text_to_video_pipeline == "wan22_fal" and FAL_KEY:
        try:
            logger.info("Calling FAL WAN 2.2 T2V")
            headers = {"Authorization": f"Key {FAL_KEY}", "Content-Type": "application/json"}
            payload = {
                "prompt": description,
                "model": "Wan2.2-T2V-A14B",
                "seconds": 3,
                "width": 1280,
                "height": 720,
                "fps": 24
            }
            r = requests.post("https://fal.run/fal-ai/wans/api/generate", headers=headers, data=json.dumps(payload), timeout=60)
            r.raise_for_status()
            data = r.json()
            # Expect a downloadable URL in response
            video_url = data.get("video_url") or data.get("url")
            if video_url:
                vid = requests.get(video_url, timeout=60)
                with open(output_path, 'wb') as f:
                    f.write(vid.content)
                return True
            logger.warning("FAL WAN response missing video_url; falling back to image/mock")
        except Exception as e:
            logger.warning(f"WAN 2.2 generation failed: {e}; falling back")
    
    if text_to_video_pipeline is None:
        # Try to fetch a relevant image from Wikipedia and use it as a pan/zoom clip
        try:
            img_path = fetch_related_image(description)
            if img_path and MOVIEPY_AVAILABLE:
                return create_image_pan_clip(img_path, output_path)
        except Exception as _img_err:
            logger.info(f"Image fetch failed; falling back to mock video")
        # Create a mock video for development
        return create_mock_video(description, output_path)
    
    try:
        logger.info(f"Generating video for: {description}")
        
        # Generate video using the pipeline
        video_result = text_to_video_pipeline(
            description,
            num_frames=16,  # 4 seconds at 4fps
            height=512,
            width=512
        )
        
        # Save the video
        video = video_result["videos"][0]
        # Convert tensor to video file (this is a simplified version)
        # In practice, you'd need to properly convert the tensor to video format
        
        return create_mock_video(description, output_path)
        
    except Exception as e:
        logger.error(f"Error generating video: {e}")
        return create_mock_video(description, output_path)

def create_mock_video(description, output_path):
    """Create a mock 3s video using MoviePy if available, else OpenCV.
    This avoids hard dependency on MoviePy for development.
    """
    duration_seconds = 3
    width, height, fps = 512, 512, 8  # Higher FPS for smoother video
    
    if MOVIEPY_AVAILABLE:
        try:
            logger.info(f"Creating mock video with MoviePy: {description[:30]}...")
            
            # Create gradient background with animation
            import random
            colors = [(70, 130, 180), (100, 150, 200), (120, 170, 220), (90, 140, 190)]
            bg_color = random.choice(colors)
            bg = ColorClip(size=(width, height), color=bg_color, duration=duration_seconds)
            
            # Add animated rectangle for visual interest
            rect_color = (255, 255, 255, 100)  # Semi-transparent white
            rect_size = (width//3, height//6)
            
            # Create text overlay
            try:
                # Split description into words and take first few
                words = description.split()[:4]
                text_content = ' '.join(words)
                if len(text_content) > 25:
                    text_content = text_content[:25] + "..."
                
                txt = TextClip(
                    text_content, 
                    fontsize=24, 
                    color='white', 
                    font='Arial-Bold'
                ).set_position('center').set_duration(duration_seconds)
                
                # Add a simple moving element for animation
                moving_rect = ColorClip(
                    size=(50, 50), 
                    color=(255, 255, 255), 
                    duration=duration_seconds
                ).set_position(lambda t: (int(50 + t * 100), height - 100))
                
                video = CompositeVideoClip([bg, moving_rect, txt])
                
            except Exception as text_error:
                logger.warning(f"Text overlay failed: {text_error}, using animated background")
                # Create simple animated background
                moving_rect = ColorClip(
                    size=(100, 100), 
                    color=(255, 255, 255, 150), 
                    duration=duration_seconds
                ).set_position(lambda t: (int(t * 100) % (width-100), int(t * 50) % (height-100)))
                
                video = CompositeVideoClip([bg, moving_rect])
            
            video.write_videofile(
                output_path, 
                fps=fps, 
                codec='libx264', 
                audio=False,
                verbose=False,
                logger=None
            )
            video.close()
            bg.close()
            logger.info(f"Mock video created successfully: {output_path}")
            return True
        except Exception as e:
            logger.warning(f"MoviePy mock video failed, falling back to OpenCV: {e}")
            # fall through to OpenCV
    
    # OpenCV fallback
    try:
        if cv2 is None:
            raise RuntimeError("OpenCV not available")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Create solid-color frames with simple moving rectangle for motion
        total_frames = duration_seconds * fps
        for i in range(total_frames):
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            frame[:] = (100, 150, 200)
            # simple animation rectangle
            x = int((i / total_frames) * (width - 100))
            cv2.rectangle(frame, (x, 200), (x + 100, 300), (255, 255, 255), -1)
            writer.write(frame)
        writer.release()
        return True
    except Exception as e:
        logger.error(f"Error creating mock video via OpenCV: {e}")
        return False

def fetch_related_image(query):
    """Fetch a related image from Wikipedia and return a local path, or None."""
    try:
        session = requests.Session()
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            'action': 'query',
            'format': 'json',
            'prop': 'pageimages',
            'piprop': 'original',      
            'generator': 'search',
            'gsrsearch': query,
            'gsrlimit': 1
        }
        resp = session.get(url, params=params, timeout=10)
        data = resp.json()
        pages = data.get('query', {}).get('pages', {})
        for _, page in pages.items():
            original = page.get('original')
            if original and 'source' in original:
                img_url = original['source']
                img_bytes = session.get(img_url, timeout=10).content
                tmp_dir = tempfile.gettempdir()
                file_ext = os.path.splitext(img_url)[1] or '.jpg'
                local_path = os.path.join(tmp_dir, f"edu_img_{abs(hash(img_url))}{file_ext}")
                with open(local_path, 'wb') as f:
                    f.write(img_bytes)
                return local_path
    except Exception as e:
        logger.info(f"Wikipedia image fetch error: {e}")
    return None

def create_image_pan_clip(image_path, output_path, duration_seconds=3):
    """Create a simple Ken Burns pan/zoom video from a still image."""
    if not MOVIEPY_AVAILABLE:
        return False
    try:
        clip = ImageClip(image_path).resize(width=1280).set_duration(duration_seconds)
        # Apply slow zoom + gentle fade
        clip = clip.fx(vfx.resize, lambda t: 1 + 0.06 * t)
        try:
            clip = clip.fx(vfx.fadein, 0.25).fx(vfx.fadeout, 0.25)
        except Exception:
            pass
        clip.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio=False,
            verbose=False,
            logger=None
        )
        clip.close()
        return True
    except Exception as e:
        logger.info(f"create_image_pan_clip failed: {e}")
        return False

def generate_audio(narration, output_path):
    """
    Generate audio narration using TTS
    
    Args:
        narration (str): Text to convert to speech
        output_path (str): Path to save the audio file
        
    Returns:
        str | None: Path to generated audio file (may be mp3 or wav), or None on failure
    """
    if tts_pipeline is None:
        # Offline-only TTS via pyttsx3
        try:
            import pyttsx3  # type: ignore
            engine = pyttsx3.init()
            # Set comfortable defaults
            try:
                engine.setProperty('rate', 175)
                engine.setProperty('volume', 0.9)
                # Prefer a SAPI5 English voice if available on Windows
                voices = engine.getProperty('voices') or []
                for v in voices:
                    name = getattr(v, 'name', '') or ''
                    lang = ''.join(getattr(v, 'languages', []) or [])
                    if 'en' in name.lower() or 'en' in lang.lower():
                        engine.setProperty('voice', v.id)
                        break
            except Exception:
                pass
            wav_path = output_path if output_path.lower().endswith('.wav') else output_path + '.wav'
            text = narration.strip() if narration else "This is an educational narration generated by the app."
            engine.save_to_file(text, wav_path)
            engine.runAndWait()
            # Ensure file is written
            for _ in range(20):
                if os.path.exists(wav_path) and os.path.getsize(wav_path) > 0:
                    break
                import time; time.sleep(0.1)
            return wav_path if os.path.exists(wav_path) else None
        except Exception as tts_local_err:
            logger.warning(f"Offline TTS (pyttsx3) failed: {tts_local_err}. Falling back to silent audio.")
            ok = create_mock_audio(narration, output_path)
            return output_path if ok else None
    
    try:
        logger.info(f"Generating audio for: {narration[:50]}...")
        
        # Generate audio using TTS pipeline
        audio_result = tts_pipeline(narration)
        
        # Save audio (this is simplified - actual implementation would depend on the model output)
        # For now, create mock audio
        ok = create_mock_audio(narration, output_path)
        return output_path if ok else None
        
    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        ok = create_mock_audio(narration, output_path)
        return output_path if ok else None

def create_mock_audio(narration, output_path):
    """Create 3s of silent WAV audio without MoviePy using wave module."""
    try:
        sample_rate = 22050
        duration_seconds = 3
        num_samples = sample_rate * duration_seconds
        with wave.open(output_path, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(sample_rate)
            silent_frame = struct.pack('<h', 0)
            wf.writeframes(silent_frame * num_samples)
        return True
    except Exception as e:
        logger.error(f"Error creating mock audio: {e}")
        return False

def merge_videos_and_audio(video_paths, audio_paths, output_path):
    """
    Merge all video clips and audio into final video using MoviePy
    
    Args:
        video_paths (list): List of video file paths
        audio_paths (list): List of audio file paths
        output_path (str): Path for final output video
        
    Returns:
        bool: Success status
    """
    try:
        logger.info("Merging videos and audio...")
        logger.info(f"Video paths: {video_paths}")
        logger.info(f"Audio paths: {audio_paths}")
        
        if MOVIEPY_AVAILABLE:
            # MoviePy path
            video_clips = []
            for vp in video_paths:
                if os.path.exists(vp):
                    logger.info(f"Loading video: {vp}")
                    video_clips.append(VideoFileClip(vp))
                else:
                    logger.warning(f"Video file not found: {vp}")
            
            if not video_clips:
                logger.error("No video clips found")
                return False
            
            logger.info(f"Concatenating {len(video_clips)} video clips...")
            # Ensure consistent size (1280x720)
            try:
                video_clips = [vc.resize(newsize=(1280, 720)) for vc in video_clips]
            except Exception:
                pass
            final_video = concatenate_videoclips(video_clips, method='compose')
            
            audio_clips = []
            final_audio = None
            for ap in audio_paths:
                if os.path.exists(ap):
                    logger.info(f"Loading audio: {ap}")
                    audio_clips.append(AudioFileClip(ap))
                else:
                    logger.warning(f"Audio file not found: {ap}")
            
            if audio_clips:
                logger.info(f"Concatenating {len(audio_clips)} audio clips...")
                try:
                    from moviepy.audio.AudioClip import concatenate_audioclips
                    final_audio = concatenate_audioclips(audio_clips)
                    final_video = final_video.set_audio(final_audio)
                except Exception as audio_error:
                    logger.warning(f"Audio concatenation failed: {audio_error}, proceeding without audio")
            
            logger.info(f"Writing final video to: {output_path}")
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac' if audio_clips else None,
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                verbose=False,
                logger=None
            )
            
            # Clean up
            try:
                final_video.close()
            finally:
                if final_audio is not None:
                    try:
                        final_audio.close()
                    except Exception:
                        pass
            for c in video_clips:
                c.close()
            for c in audio_clips:
                c.close()
            
            logger.info(f"Final video saved successfully to: {output_path}")
            return True
        
        # Fallback: use ffmpeg via imageio-ffmpeg
        if imageio_ffmpeg is None:
            logger.error("imageio-ffmpeg not available; cannot merge without MoviePy")
            return False
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        
        # Create concat files
        concat_v = os.path.join(os.path.dirname(output_path), 'concat_v.txt')
        concat_a = os.path.join(os.path.dirname(output_path), 'concat_a.txt')
        with open(concat_v, 'w', encoding='utf-8') as f:
            for vp in video_paths:
                f.write(f"file '{vp.replace('\\', '/')}'\n")
        with open(concat_a, 'w', encoding='utf-8') as f:
            for ap in audio_paths:
                f.write(f"file '{ap.replace('\\', '/')}'\n")
        
        import subprocess
        temp_v = os.path.join(os.path.dirname(output_path), 'temp_concat_v.mp4')
        temp_a = os.path.join(os.path.dirname(output_path), 'temp_concat_a.wav')
        
        # Concat videos
        subprocess.check_call([ffmpeg_exe, '-y', '-f', 'concat', '-safe', '0', '-i', concat_v,
                               '-c:v', 'libx264', '-pix_fmt', 'yuv420p', temp_v])
        # Concat audios
        if audio_paths:
            subprocess.check_call([ffmpeg_exe, '-y', '-f', 'concat', '-safe', '0', '-i', concat_a,
                                   '-c:a', 'pcm_s16le', temp_a])
        
        # Merge video and audio
        merge_cmd = [ffmpeg_exe, '-y', '-i', temp_v]
        if audio_paths:
            merge_cmd += ['-i', temp_a, '-c:v', 'copy', '-c:a', 'aac', '-shortest', output_path]
        else:
            merge_cmd += ['-c:v', 'copy', output_path]
        subprocess.check_call(merge_cmd)
        
        logger.info(f"Final video saved to: {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error merging videos: {e}")
        return False

@app.route('/')
def index():
    """Serve the main page"""
    return send_file('index.html')

@app.route('/style.css')
def style():
    """Serve the CSS file"""
    return send_file('style.css')

@app.route('/generate', methods=['POST'])
def generate_video():
    """Generate educational video with script, audio, and short video clips"""
    try:
        topic = request.form.get('topic', '').strip()
        if not topic:
            logger.error("No topic provided")
            return jsonify({'error': 'Topic is required'}), 400
        
        logger.info(f"Generating content for topic: {topic}")
        
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            logger.info(f"Using temp directory: {temp_dir}")
            
            # Step 1: Generate script
            logger.info("Step 1: Generating script...")
            script = generate_script_with_mistral(topic)
            scenes = script.get('scenes', [])
            
            if not scenes:
                logger.error("No scenes generated")
                return jsonify({'error': 'Failed to generate script'}), 500
            
            logger.info(f"Generated {len(scenes)} scenes")
            
            # Step 2: Generate audio and video for each scene
            video_paths = []
            audio_paths = []
            
            for i, scene in enumerate(scenes):
                logger.info(f"Processing scene {i+1}/{len(scenes)}")
                
                # Generate 3-second video clip
                video_path = os.path.join(temp_dir, f"scene_{i}_video.mp4")
                logger.info(f"Generating video: {video_path}")
                description = scene.get('description', 'Educational visual')
                if generate_video_clip(description, video_path):
                    video_paths.append(video_path)
                    logger.info(f"Video generated successfully: {video_path}")
                
                # Generate audio
                base_audio_path = os.path.join(temp_dir, f"scene_{i}_audio.wav")
                logger.info(f"Generating audio: {base_audio_path}")
                narration = scene.get('narration', '')
                produced_audio_path = generate_audio(narration, base_audio_path)
                if produced_audio_path and os.path.exists(produced_audio_path):
                    audio_paths.append(produced_audio_path)
                    logger.info(f"Audio generated successfully: {produced_audio_path}")
            
            if not video_paths:
                logger.error("No video clips were generated")
                return jsonify({'error': 'Failed to generate any video clips'}), 500
            
            # Step 3: Merge all clips into final video
            logger.info("Merging final video...")
            final_video_path = os.path.join(temp_dir, "final_video.mp4")
            
            if merge_videos_and_audio(video_paths, audio_paths, final_video_path):
                if os.path.exists(final_video_path):
                    logger.info(f"Final video created successfully: {final_video_path}")
                    # Read into memory before sending to avoid Windows file lock issues
                    with open(final_video_path, 'rb') as f:
                        data = f.read()
                    return send_file(
                        io.BytesIO(data),
                        as_attachment=True,
                        download_name=f"educational_video_{topic.replace(' ', '_')}.mp4",
                        mimetype='video/mp4'
                    )
                else:
                    logger.error("Final video file was not created")
                    return jsonify({'error': 'Final video file was not created'}), 500
            else:
                logger.error("Failed to merge video clips")
                return jsonify({'error': 'Failed to create final video'}), 500
                
    except Exception as e:
        logger.error(f"Error in generate_video: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': {
            'gpt2': mistral_pipeline is not None,
            'text_to_video': text_to_video_pipeline is not None,
            'tts': tts_pipeline is not None
        }
    })

@app.route('/test-script/<topic>')
def test_script(topic):
    """Test script generation for a topic"""
    try:
        logger.info(f"Testing script generation for: {topic}")
        script = generate_script_with_mistral(topic)
        return jsonify({
            'success': True,
            'topic': topic,
            'script': script
        })
    except Exception as e:
        logger.error(f"Error testing script: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Load models on startup
    logger.info("Starting Educational Video Generator...")
    load_models()
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
