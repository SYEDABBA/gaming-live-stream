import os
import subprocess
import sys
import re

def download_video_with_curl():
    video_id = "1jXxRR2tpQXNrwj_jeK2DS0o-sHovkvzE"
    output_file = "stream_video.mp4"
    
    if os.path.exists(output_file):
        print("✅ Video pehle se downloaded hai.")
        return
        
    print("📥 Google Drive virus warning bypass karke download shuru ho raha hai...")
    
    # Step 1: Ek cookie file generate karke confirmation code nikalna
    # Isse Google Drive ko lagega ki humne warning read karke 'Download Anyway' par click kar diya hai
    cookie_file = "cookies.txt"
    
    # Pehla hit: confirmation code nikalne ke liye
    cmd_confirm = f'curl -c {cookie_file} -s -L "https://docs.google.com/uc?export=download&id={video_id}"'
    response = subprocess.check_output(cmd_confirm, shell=True).decode('utf-8', errors='ignore')
    
    # HTML me se confirmation token dundhna (e.g., confirm=t ooxx)
    match = re.search(r'confirm=([0-9A-Za-z_]+)', response)
    
    if match:
        confirm_token = match.group(1)
        print(f"🔑 Confirmation token mil gaya: {confirm_token}")
        download_url = f"https://docs.google.com/uc?export=download&confirm={confirm_token}&id={video_id}"
    else:
        print("⚠️ Direct confirmation token nahi mila, standard query try kar rahe hain...")
        download_url = f"https://docs.google.com/uc?export=download&id={video_id}"
        
    # Step 2: Actual video file download karna cookies ke saath
    print("🚀 Video file chunk-by-chunk download ho rahi hai...")
    curl_download = [
        "curl",
        "-b", cookie_file,
        "-L",
        "-o", output_file,
        download_url
    ]
    
    result = subprocess.run(curl_download)
    
    # Clean up cookies file
    if os.path.exists(cookie_file):
        os.remove(cookie_file)
        
    if result.returncode == 0 and os.path.exists(output_file) and os.path.getsize(output_file) > 1000000:
        file_size_gb = os.path.getsize(output_file) / (1024 * 1024 * 1024)
        print(f"✅ Success! Real Video downloaded: {output_file} ({file_size_gb:.2f} GB)")
    else:
        print("❌ Download fail ho gaya ya corrupt file aayi hai.")
        if os.path.exists(output_file):
            print(f"File Size: {os.path.getsize(output_file)} bytes (Agar yeh chota hai, toh yeh video nahi text file hai)")
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
    download_video_with_curl()
    start_live_stream()
