import os
import subprocess
import sys
import re
import requests

def download_video_with_session():
    video_id = "1jXxRR2tpQXNrwj_jeK2DS0o-sHovkvzE"
    output_file = "stream_video.mp4"
    
    if os.path.exists(output_file) and os.path.getsize(output_file) > 10000000:
        print("✅ Video pehle se downloaded hai.")
        return
        
    print("📥 Browser Session banakar download shuru ho raha hai...")
    
    # Ek session create karenge taaki cookies automatic handle ho sakein
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    
    base_url = "https://docs.google.com/uc?export=download"
    
    # Step 1: Pehli request warning page hit karne ke liye
    response = session.get(base_url, params={"id": video_id}, stream=True)
    
    token = None
    # Method A: Google ke set kiye hue download_warning cookie se token nikalna
    for key, value in session.cookies.items():
        if key.startswith("download_warning"):
            token = value
            break
            
    # Method B: Agar cookie me nahi mila, toh HTML text me se dundhna
    if not token:
        html_content = response.text
        match = re.search(r'confirm=([0-9A-Za-z_\-]+)', html_content)
        if match:
            token = match.group(1)
            
    # Step 2: Confirmation token ke saath actual download trigger karna
    if token:
        print(f"🔑 Success! Confirmation token mil gaya: {token}")
        confirm_params = {"id": video_id, "confirm": token}
        download_response = session.get(base_url, params=confirm_params, stream=True)
    else:
        print("⚠️ Warning: Token nahi mila, direct download try kar rahe hain...")
        download_response = session.get(base_url, params={"id": video_id}, stream=True)
        
    # Step 3: File save karna chunks me
    print("🚀 Video file chunk-by-chunk download ho rahi hai...")
    with open(output_file, "wb") as f:
        for chunk in download_response.iter_content(chunk_size=1024 * 1024): # 1MB Chunks
            if chunk:
                f.write(chunk)
                
    if os.path.exists(output_file) and os.path.getsize(output_file) > 10000000:
        file_size_gb = os.path.getsize(output_file) / (1024 * 1024 * 1024)
        print(f"✅ BINGO! Asli video download ho gayi: {output_file} ({file_size_gb:.2f} GB)")
    else:
        print("❌ Download fail ho gaya.")
        if os.path.exists(output_file):
            print(f"Downloaded file size: {os.path.getsize(output_file)} bytes")
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
        "-stream_loop", "-1",
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
    download_video_with_session()
    start_live_stream()
