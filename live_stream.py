import os
import subprocess
import sys
import time

def download_video_with_gdown():
    video_id = "1jXxRR2tpQXNrwj_jeK2DS0o-sHovkvzE"
    print(f"⏳ Target File ID: {video_id}")
    
    # Install gdown quietly
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "gdown"])
    
    output_file = "stream_video.mp4"
    if os.path.exists(output_file):
        print("✅ Video pehle se downloaded hai.")
        return
        
    print("📥 gdown se video download ho rahi hai...")
    gdown_cmd = ["gdown", "--id", video_id, "-O", output_file, "--remaining-ok"]
    result = subprocess.run(gdown_cmd)
    
    if result.returncode == 0 and os.path.exists(output_file):
        print(f"✅ Success! Video download ho gayi: {output_file}")
    else:
        print("❌ Download fail hua!")
        sys.exit(1)

def start_live_stream():
    stream_url = "rtmp://a.rtmp.youtube.com/live2"
    stream_key = os.environ.get("YT_STREAM_KEY")
    
    if not stream_key:
        print("❌ Error: YT_STREAM_KEY nahi mili!")
        sys.exit(1)
        
    full_stream_path = f"{stream_url}/{stream_key.strip()}"
    
    # FFmpeg standard continuous stream configuration
    ffmpeg_cmd = [
        "ffmpeg",
        "-nostdin",                     # Very Important: Terminal input errors se bachata hai
        "-re",
        "-stream_loop", "-1",           # Infinite loop
        "-i", "stream_video.mp4",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-b:v", "3000k",
        "-maxrate", "3000k",
        "-bufsize", "6000k",
        "-pix_fmt", "yuv420p",
        "-g", "60",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "44100",
        "-f", "flv",
        full_stream_path
    ]
    
    print("📺 YUGRAAL Live Engine: Pushing stream to YouTube...")
    
    # Run synchronously to hold the GitHub Action workflow alive
    process = subprocess.run(ffmpeg_cmd)
    
    # Agar kisi wajah se stop ho jaye toh auto-restart lagane ke liye infinite hold:
    if process.returncode != 0:
        print("⚠️ Stream dropped. Restarting workflow hook...")
        sys.exit(1)

if __name__ == "__main__":
    download_video_with_gdown()
    start_live_stream()
