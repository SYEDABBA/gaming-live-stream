import os
import subprocess
import requests

def download_video_from_drive():
    video_id = os.environ.get("STREAM_VIDEO_ID")
    refresh_token = os.environ.get("GD_REFRESH_TOKEN")
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    
    print("⏳ Google Drive se naya token request ho raha hai...")
    
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "client_id": client_id.strip() if client_id else "",
        "client_secret": client_secret.strip() if client_secret else "",
        "refresh_token": refresh_token.strip() if refresh_token else "",
        "grant_type": "refresh_token"
    }
    
    r = requests.post(token_url, data=token_data)
    response_json = r.json()
    
    if "access_token" not in response_json:
        print(f"❌ Token Exchange Failed! Google Response: {response_json}")
        exit(1)
        
    access_token = response_json.get("access_token")
    print("✅ Access Token mil gaya! Large video file download shuru ho rahi hai...")
    
    # Large files download karne ke liye exact reliable endpoint url:
    download_url = f"https://www.googleapis.com/drive/v3/files/{video_id.strip()}"
    params = {"alt": "media"}
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Stream set kiya hai taaki RAM crash na ho aur chunk by chunk download ho
    response = requests.get(download_url, headers=headers, params=params, stream=True)
    
    if response.status_code == 200:
        print("📥 Data blocks mil rahe hain, local file me write ho raha hai...")
        with open("stream_video.mp4", "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024): # 1MB chunks
                if chunk:
                    f.write(chunk)
        print("✅ 1.39 GB Video perfectly download ho gayi!")
    else:
        print(f"❌ Download failed! Status code: {response.status_code}")
        print(f"Google Drive Response: {response.text}")
        exit(1)

def start_live_stream():
    stream_url = "rtmp://a.rtmp.youtube.com/live2"
    stream_key = os.environ.get("YT_STREAM_KEY")
    
    if not stream_key:
        print("❌ Error: YT_STREAM_KEY nahi mili!")
        exit(1)
        
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
    
    print("📺 FFmpeg Engine Active: Live push shuru ho raha hai...")
    subprocess.run(ffmpeg_cmd)

if __name__ == "__main__":
    download_video_from_drive()
    start_live_stream()
