import os
import subprocess
import requests

def download_video_from_drive():
    video_id = os.environ.get("STREAM_VIDEO_ID")
    refresh_token = os.environ.get("GD_REFRESH_TOKEN")
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    
    print("⏳ Google Drive se video download ho rahi hai...")
    
    # Access Token lena
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"  # <-- YAHAN FIX KIYA HAI!
    }
    r = requests.post(token_url, data=token_data)
    
    # Debug karne ke liye response check karna
    response_json = r.json()
    access_token = response_json.get("access_token")
    
    if not access_token:
        print(f"❌ Token Exchange Failed! Response: {response_json}")
        exit(1)
    
    # File download karna
    download_url = f"https://www.googleapis.com/drive/v3/files/{video_id}?alt=media"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(download_url, headers=headers, stream=True)
    if response.status_code == 200:
        with open("stream_video.mp4", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print("✅ Video successfully download ho gayi: stream_video.mp4")
    else:
        print(f"❌ Download failed! Status code: {response.status_code}")
        exit(1)

def start_live_stream():
    stream_url = "rtmp://a.rtmp.youtube.com/live2"
    stream_key = os.environ.get("YT_STREAM_KEY")
    
    if not stream_key:
        print("❌ Error: YT_STREAM_KEY nahi mili!")
        exit(1)
        
    full_stream_path = f"{stream_url}/{stream_key}"
    
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
    
    print("📺 FFmpeg Live stream shuru kar raha hai... YouTube Dashboard check karo!")
    subprocess.run(ffmpeg_cmd)

if __name__ == "__main__":
    download_video_from_drive()
    start_live_stream()
