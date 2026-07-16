import os
import subprocess
import sys

def download_video_with_curl():
    video_id = "1jXxRR2tpQXNrwj_jeK2DS0o-sHovkvzE"
    output_file = "stream_video.mp4"
    
    if os.path.exists(output_file):
        print("✅ Video pehle se downloaded hai.")
        return
        
    print("📥 Direct curl method se video download shuru ho rahi hai...")
    
    # Direct browser simulation link for large drive files
    download_url = f"https://docs.google.com/uc?export=download&id={video_id}&confirm=t"
    
    # curl command jo large files ko seamlessly block-by-block download karti hai
    curl_cmd = [
        "curl", 
        "-L", 
        "-o", output_file, 
        download_url
    ]
    
    result = subprocess.run(curl_cmd)
    
    if result.returncode == 0 and os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        print(f"✅ Success! Video perfectly download ho gayi via curl: {output_file}")
    else:
        print("❌ Curl method fail hua! Secondary direct fetch try kar rahe hain...")
        fallback_url = f"https://drive.google.com/uc?export=download&id={video_id}"
        subprocess.run(["curl", "-L", "-o", output_file, fallback_url])
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print("✅ Video downloaded via fallback curl!")
        else:
            print("❌ Dono methods fail ho gaye.")
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
    download_video_with_curl()
    start_live_stream()
