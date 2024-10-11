import requests
from concurrent.futures import ThreadPoolExecutor

urls = [
    "https://streamtape.net/get_video?id=eobd2VqRp3FYlz3&expires=1720680980&ip=F0IQKROTKxSHDN&token=uHK0Kv1xlre9&stream=1"
]

chunk_size = 1024 * 1024  # 1 MB

def download_file(url):
    local_filename = url.split("id=")[-1].split("&")[0] + ".mp4"  # Generate a filename based on the URL
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            total_downloaded = 0
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:  # Filter out keep-alive new chunks
                        f.write(chunk)
                        total_downloaded += len(chunk)
                        progress = (total_downloaded / total_size) * 100
                        print(f"Downloading {local_filename}: {progress:.2f}%")
        print(f"Download of {local_filename} completed successfully")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading {local_filename}: {e}")

# Use ThreadPoolExecutor to download files concurrently
max_workers = min(4, len(urls))  # Limit to 4 threads or number of URLs if less
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(download_file, urls)








