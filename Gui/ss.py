import yt_dlp

def search_videos(query, max_results=25):
    search_url = f"ytsearch{max_results}:{query}"
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_url, download=False)
        return [  entry['url'] for entry in info['entries']]

keyword = input("Enter search keyword: ")
videos = search_videos(keyword)

print("\nSearch results:")
for  url in videos:
    print(f" {url}")