import os
import subprocess
import sys

def download_video_with_gdown():
    video_id = "1jXxRR2tpQXNrwj_jeK2DS0o-sHovkvzE"
    print(f"⏳ Target File ID: {video_id}")
    
    # Quietly install gdown
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "gdown"])
    
    output_file = "stream_video.mp4"
    if os.path.exists(output_file):
        print("✅ Video pehle se downloaded hai.")
        return
        
    print("📥 gdown se video download ho rahi hai...")
    
    # Naya and simple direct link format jo har version ke gdown me chalta hai
    drive_link = f"https://drive.google.com/uc?id={video_id}"
    gdown_cmd = ["gdown", drive_link, "-O", output_file]
    
    result = subprocess.run(gdown_cmd)
    
    if result.returncode == 0 and os.path.exists(output_file):
        print(f"✅ Success! Video download ho gayi: {output_file}")
    else:
        print("❌ Download fail hua! Alternative method try karte hain...")
        sys.exit(1)

def start_live_stream():
    stream_url = "rtmp://a.rtmp.youtube.com/live2"
    stream_key = os.environ.get("YT_STREAM_KEY")
    
    if not stream_key:
        print("❌ Error: YT_STREAM_KEY nahi mili!")
        sys.exit(1)
        
    full_stream_path = f"{stream_url}/{stream_key.strip()}"
    
    ffmpeg_cmd = [
        "ffmpeg",
        "-nostdin",
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
    process = subprocess.run(ffmpeg_cmd)
    
    if process.returncode != 0:
        print("⚠️ Stream dropped.")
        sys.exit(1)

if __name__ == "__main__":
    download_video_with_gdown()
    start_live_stream()
