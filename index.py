import requests
from bs4 import BeautifulSoup
import json
import os
import moviepy.editor as mp
def get_video_urls(mid):
    url = f'https://api.bilibili.com/x/space/arc/search?mid={mid}&ps=30&tid=0&pn=1&order=pubdate'
    try:
        response = requests.get(url)
        data = json.loads(response.text)
        video_urls = []
        for item in data['data']['list']:
            video_urls.append(item['bvid'])
        return video_urls
    except Exception as e:
        print(f"Error occurred while getting video urls: {e}")
        return []
def download_video(url, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers)
        with open(filename, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print(f"Error occurred while downloading video: {e}")
def mix_videos(video_urls, music_url, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    video_clips = []
    for url in video_urls:
        video_clip = mp.VideoFileClip(download_video(url, os.path.join(output_dir, f'{url}.mp4')))
        video_clips.append(video_clip)
    final_clip = mp.concatenate_videoclips(video_clips)
    final_clip = final_clip.set_audio(mp.AudioFileClip(music_url))
    try:
        final_clip.write_videofile(os.path.join(output_dir, 'mixed_video.mp4'))
    except Exception as e:
        print(f"Error occurred while writing video file: {e}")
if __name__ == '__main__':
    mid = input('请输入Up主的mid:')
    music_url = input('请输入音乐文件的URL:')
    output_dir = input('请输入输出文件夹路径：')
    video_urls = get_video_urls(mid)
    if video_urls:
        mix_videos(video_urls, music_url, output_dir)
        print('混剪完成！')
    else:
        print('未找到有效的视频！')
