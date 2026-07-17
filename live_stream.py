import os
import subprocess
import sys
import urllib.request

def download_video_direct():
    # Dropbox link modified with dl=1 for instant direct download
    direct_video_url = "https://www.dropbox.com/scl/fi/9glapboibpvfs3vkg3qji/Spider-Man-2-Stealth-on-Max-Settings-Looks-Unreal-720P_HD.mp4?rlkey=b5929gj61xjwb9y4wh6t09c57&st=1gtbobyg&dl=1" 
    
    output_file = "stream_video.mp4"
    
    if os.path.exists(output_file) and os.path.getsize(output_file) > 5000000:
        print("✅ Video pehle se downloaded hai.")
        return
        
    print("📥 Dropbox direct URL se video download shuru ho rahi hai...")
    
    try:
        # User-Agent header add kiya hai taaki Dropbox request ko block na kare
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]
        urllib.request.install_opener(opener)
        
        # Fast direct download
        urllib.request.urlretrieve(direct_video_url, output_file)
        
        if os.path.exists(output_file) and os.path.getsize(output_file) > 5000000:
            file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"✅ BINGO! Asli video perfectly download ho gayi: {output_file} ({file_size_mb:.2f} MB)")
        else:
            print("❌ Download fail ho gaya ya file ka size bohot chota hai.")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error downloading file: {e}")
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
        "-stream_loop", "-1",           # Infinite loop me chalta rahega
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
    download_video_direct()
    start_live_stream()
