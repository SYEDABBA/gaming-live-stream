import os
import subprocess
import sys

def download_video_with_gdown():
    video_id = os.environ.get("STREAM_VIDEO_ID")
    if not video_id:
        print("❌ Error: STREAM_VIDEO_ID GitHub Secrets me nahi mili!")
        sys.exit(1)
        
    video_id = video_id.strip()
    print(f"⏳ Target File ID: {video_id}")
    print("📦 gdown library install ho rahi hai...")
    
    # gdown install karna jo large drive files ke liye best hai
    subprocess.run([sys.executable, "-m", "pip", "install", "gdown"])
    
    print("📥 gdown se direct large file download shuru ho rahi hai...")
    
    # Direct command line download pipeline
    output_file = "stream_video.mp4"
    gdown_cmd = ["gdown", "--id", video_id, "-O", output_file, "--remaining-ok"]
    
    result = subprocess.run(gdown_cmd)
    
    if result.returncode == 0 and os.path.exists(output_file):
        print(f"✅ Success! 1.39 GB Video perfectly download ho gayi: {output_file}")
    else:
        print("❌ gdown download fail hua! Alternative browser route try kar rahe hain...")
        import requests
        download_url = f"https://docs.google.com/uc?export=download&id={video_id}&confirm=t"
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            with open(output_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            print("✅ Video successfully downloaded via alternative route!")
        else:
            print(f"❌ Dono methods fail ho gaye. Status: {response.status_code}")
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
    
    print("📺 FFmpeg Engine Active: Live stream push shuru ho raha hai...")
    subprocess.run(ffmpeg_cmd)

if __name__ == "__main__":
    download_video_with_gdown()
    start_live_stream()
