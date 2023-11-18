import requests
import json
import pandas as pd
from datetime import datetime, timedelta

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'AIzaSyCsBnmdjr2SDnjuL5ZTIp-6UbOAQ4aNt3A'

# Function to get video information by channel ID
def get_channel_videos(channel_id):
    url = f'https://www.googleapis.com/youtube/v3/search?key={API_KEY}&part=snippet&channelId={channel_id}&order=viewCount&maxResults=10&type=video'
    response = requests.get(url)
    data = json.loads(response.text)
    return data['items'] if 'items' in data else None

# Function to get detailed video statistics by video ID
def get_video_statistics(video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos?key={API_KEY}&part=statistics&id={video_id}'
    response = requests.get(url)
    data = json.loads(response.text)
    return data['items'][0]['statistics'] if 'items' in data else None

def append_video_data(csv_file, video_data):
    # Đọc dữ liệu hiện tại từ file CSV (nếu có)
    try:
        existing_data = pd.read_csv(csv_file)
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    # Kiểm tra xem từng 'id' trong 'video_data' đã tồn tại trong dữ liệu hiện tại chưa
    existing_ids = set(existing_data['id']) if 'id' in existing_data.columns else set()
    new_video_data = [item for item in video_data if item['id'] not in existing_ids]

    if not new_video_data:
        print("All video information already exists. Skipping.")
    else:
        # Thêm dữ liệu mới vào dữ liệu hiện tại
        video_data_df = pd.DataFrame(new_video_data)
        updated_data = pd.concat([existing_data, video_data_df], ignore_index=True)

        # Ghi dữ liệu đã cập nhật vào file CSV
        updated_data.to_csv(csv_file, index=False)
        print("Video information saved successfully.")

# Đọc dữ liệu từ file CSV vào DataFrame
df = pd.read_csv('DataYoutubeTrending.csv')
keywords = [
    'health', 'fitness', 'wellness', 'beauty', 'skincare', 'nutrition', 'exercise',
    'education', 'learning', 'personal development', 'self-improvement', 'skills development', 'knowledge',
    'art', 'culture', 'creativity', 'literature', 'music', 'film', 'performance',
    'family', 'relationships', 'parenting', 'marriage', 'communication', 'love',
    'business', 'career', 'entrepreneurship', 'leadership', 'success', 'innovation',
    'entertainment', 'relaxation', 'hobbies', 'games', 'humor', 'movies', 'travel',
    'science', 'technology', 'innovation', 'discovery', 'research', 'gadgets',
    'psychology', 'mental health', 'mindfulness', 'meditation', 'happiness', 'stress management',
    'social issues', 'activism', 'equality', 'diversity', 'peace', 'community',
    'sports', 'outdoor activities', 'adventure', 'fitness sports', 'recreational activities'
]

# Số lượng channelId bạn muốn lấy cho mỗi từ khóa
num_channels_per_keyword = 5

# Hàm để lấy danh sách các channelId ngẫu nhiên
def get_random_channel_ids(api_key, queries, num_channels_per_query=5):
    all_channel_ids = []

    for query in queries:
        url = f'https://www.googleapis.com/youtube/v3/search?key={api_key}&part=id&type=channel&q={query}&maxResults={num_channels_per_query}&regionCode=VN'
        response = requests.get(url)
        data = json.loads(response.text)

        # Lấy `channelId` từ kết quả tìm kiếm
        if 'items' in data:
            channel_ids = [item['id']['channelId'] for item in data['items']]
            all_channel_ids.extend(channel_ids)

    return all_channel_ids

# Lấy danh sách các channelId ngẫu nhiên
# random_channel_ids = get_random_channel_ids(API_KEY, keywords, num_channels_per_keyword)

# Lấy danh sách các giá trị duy nhất từ cột "ChannelId"
channel_ids = df['channelId'].unique()
# channel_ids = random_channel_ids.unique()
# channel_ids = ['UC-lHJZR3Gqxm24_Vd_AJ5Yw', 'UC_x5XG1OV2P6uZZ5FSM9Ttw']  # Replace with your channel IDs
csv_file = 'DataVideo.csv'

for channel_id in channel_ids:
    # Get videos for the channel
    videos = get_channel_videos(channel_id)
    print(videos)
    if videos:
        # Create a list to stre video information
        video_data = []
        # Process video information and append to the list
        for video in videos:
            video_id = video['id']['videoId']
            title = video['snippet']['title']
            description = video['snippet']['description'].replace('\n', ' ')
            published_at = video['snippet']['publishedAt']
            channelTitle = video['snippet']['channelTitle']
            view_count = 0
            like_count = 0
            comment_count = 0

            # Fetch detailed statistics for each video
            video_stats = get_video_statistics(video_id)

            if video_stats:
                view_count = int(video_stats.get('viewCount', 0))
                like_count = int(video_stats.get('likeCount', 0))
                comment_count = int(video_stats.get('commentCount', 0))
            # Fetch tags for each video
            tags_url = f'https://www.googleapis.com/youtube/v3/videos?key={API_KEY}&part=snippet,contentDetails&id={video_id}'
            tags_response = requests.get(tags_url)
            tags_data = json.loads(tags_response.text)
            
            if 'items' in tags_data and 'tags' in tags_data['items'][0]['snippet']:
                tags = tags_data['items'][0]['snippet']['tags']
                dimension = tags_data['items'][0]['contentDetails']['duration']
                # print(tags)
            video_data.append({
                'id': video_id,
                'publishedAt': published_at,
                'channelId':channel_id,
                'title': title,
                'channelTitle':channelTitle,
                'tags':tags,
                'dimension':dimension,
                'description': description,
                'viewCount': view_count,
                'likeCount': like_count,
                'commentCount': comment_count
            })
        # Append video data to the CSV file
        append_video_data(csv_file, video_data)
    else:
        print(f"No videos found for channel with ID {channel_id}")
