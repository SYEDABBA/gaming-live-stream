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
        "grant_type": "refresh_grant"
    }
    r = requests.post(token_url, data=token_data)
    access_token = r.json().get("access_token")
    
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
    
    # FFmpeg command jo video ko endless loop (repeat) me live stream karegi
    ffmpeg_cmd = [
        "ffmpeg",
        "-re",                          # Real-time speed par stream karne ke liye
        "-stream_loop", "-1",           # Endless loop (-1 matlab hamesha chalta rahega)
        "-i", "stream_video.mp4",       # Input file name
        "-c:v", "libx264",              # Video codec
        "-preset", "veryfast",          # CPU standard speed
        "-b:v", "3000k",                # Video Bitrate (720p/1080p ke liye best)
        "-maxrate", "3000k",
        "-bufsize", "6000k",
        "-pix_fmt", "yuv420p",
        "-g", "60",                     # Keyframe interval
        "-c:a", "aac",                  # Audio codec
        "-b:a", "128k",                 # Audio Bitrate
        "-ar", "44100",
        "-f", "flv",                    # YouTube format
        full_stream_path                # Destination URL
    ]
    
    print("📺 FFmpeg Live stream shuru kar raha hai... YouTube Dashboard check karo!")
    subprocess.run(ffmpeg_cmd)

if __name__ == "__main__":
    download_video_from_drive()
    start_live_stream()
