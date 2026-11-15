# Human vs AI — @hi.aidelulu

A 30-second animated debate with English synthetic dialogue and burned-in captions.

- `human-vs-ai-hi-aidelulu.mp4`: downloadable vertical video, 1080 × 1920, 24 fps, H.264 video and AAC audio.
- `cover.png`: portrait cover image.
- `captions.srt`: optional separate caption file (captions are already visible in the video).
- `instagram-caption.txt`: suggested post caption and hashtags.
- `script.json`: dialogue and scene timings.
- `create_reel.py`: editable renderer, using Pillow, imageio-ffmpeg, and macOS `say` (Samantha and Daniel voices).
- `render-assets/`: intermediate voice files.

The artwork is programmatically drawn and animated. Voices are synthetic. The video has no background music and has not been posted to Instagram.

To regenerate on macOS, install Pillow and imageio-ffmpeg into a Python environment, then run `python create_reel.py`. The system speech service must be accessible; otherwise macOS can produce empty audio files.
