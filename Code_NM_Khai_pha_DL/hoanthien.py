import os
import requests
import json
import pandas as pd
from datetime import datetime, timedelta

# Thay thế 'YOUR_API_KEY' bằng khóa API của bạn
API_KEY = 'AIzaSyBNCngQRvPTXhS4QYGmuBRMHNuBb0gmCtI'

# Function to get channel information by channelId
def get_channel_info(channel_id):
    url = f'https://www.googleapis.com/youtube/v3/channels?key={API_KEY}&part=snippet,statistics&id={channel_id}'
    response = requests.get(url)
    data = json.loads(response.text)
    return data['items'][0] if 'items' in data else None

# Function to check if a channelId already exists in the CSV file
def channel_id_exists(csv_file, channel_id):
    # Kiểm tra xem file CSV đã tồn tại hay chưa
    if os.path.exists(csv_file):
        # Đọc file CSV nếu tồn tại
        df = pd.read_csv(csv_file)
    else:
        # Nếu không tồn tại, tạo DataFrame mới với các cột đã cho
        df = pd.DataFrame(columns=['channelId', 'title', 'description', 'publishedAt', 'subscriberCount', 'videoCount'])
        df.to_csv(csv_file, header=True, index=False)
        return False

    # Kiểm tra xem channelId đã tồn tại trong DataFrame hay chưa
    return channel_id in df['channelId'].values

# Function to append channel data to the CSV file
def append_channel_data(csv_file, channel_data):
    channel_data.to_csv(csv_file, mode='a', header=False, index=False)
    print(f"Channel information for {channel_data['channelTitle'].iloc[0]} saved successfully.")

# Function to get videos from the past 30 days
def get_recent_videos(api_key, desired_video_count):
    current_time = datetime.utcnow()
    start_time = current_time - timedelta(days=30)
    published_after = start_time.isoformat() + "Z"
    published_before = current_time.isoformat() + "Z"

    # Khởi tạo DataFrame trống để lưu trữ tất cả các video
    videos = pd.DataFrame()

    # Gửi yêu cầu đến YouTube Data API để lấy danh sách video phổ biến nhất
    next_page_token = None
    total_results = 0

    while total_results < desired_video_count:
        # Số lượng video còn thiếu để đạt được số lượng mong muốn
        remaining_videos = desired_video_count - total_results
        # Xác định số lượng video lấy ở mỗi trang, tối đa là 50
        videos_per_page = min(remaining_videos, 50)

        # Sử dụng publishedAfter và publishedBefore trong URL của bạn
        url = f'https://www.googleapis.com/youtube/v3/videos?key={api_key}&part=snippet,contentDetails,statistics&chart=mostPopular&regionCode=VN&maxResults=100&publishedAfter={published_after}&publishedBefore={published_before}'

        if next_page_token:
            url += f'&pageToken={next_page_token}'

        # Gửi yêu cầu API và chuyển đổi dữ liệu JSON
        response = requests.get(url)
        data = json.loads(response.text)

        # Tạo DataFrame từ thông tin video của trang hiện tại
        get50videos = pd.DataFrame(data['items'])

        # Thêm DataFrame của trang hiện tại vào DataFrame chứa tất cả video
        videos = pd.concat([videos, get50videos])

        # Cập nhật tổng số kết quả và kiểm tra xem còn trang tiếp theo không
        total_results += videos_per_page
        print(f'Total results: {total_results}')
        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            print('No more pages.')
            break

    return videos

# Example usage
csv_file = 'ChannelData.csv'

# Get recent videos
recent_videos = get_recent_videos(API_KEY, 1000)

# Chọn các cột bạn quan trọng
selected_columns = ['id']

# Tạo DataFrame mới chỉ chứa các cột bạn quan tâm
selected_videos = recent_videos[selected_columns].copy()

# Truy cập 'publishedAt' trong 'snippet'
selected_videos['publishedAt'] = recent_videos['snippet'].apply(lambda x: x['publishedAt'] if 'publishedAt' in x else '')
selected_videos['channelId'] = recent_videos['snippet'].apply(lambda x: x['channelId'] if 'channelId' in x else '')
selected_videos['title'] = recent_videos['snippet'].apply(lambda x: x['title'] if 'title' in x else '')
selected_videos['channelTitle'] = recent_videos['snippet'].apply(lambda x: x['channelTitle'] if 'channelTitle' in x else '')
selected_videos['tags'] = recent_videos['snippet'].apply(lambda x: x['tags'] if 'tags' in x else '')
selected_videos['duration'] = recent_videos['contentDetails'].apply(lambda x: x['duration'] if 'duration' in x else '')
selected_videos['dimension'] = recent_videos['contentDetails'].apply(lambda x: x['dimension'] if 'dimension' in x else '')
selected_videos['definition'] = recent_videos['contentDetails'].apply(lambda x: x['definition'] if 'definition' in x else '')
selected_videos['caption'] = recent_videos['contentDetails'].apply(lambda x: x['caption'] if 'caption' in x else '')
selected_videos['licensedContent'] = recent_videos['contentDetails'].apply(lambda x: x['licensedContent'] if 'licensedContent' in x else '')
selected_videos['contentRating'] = recent_videos['contentDetails'].apply(lambda x: x['contentRating'] if 'contentRating' in x else '')
selected_videos['projection'] = recent_videos['contentDetails'].apply(lambda x: x['projection'] if 'projection' in x else '')
selected_videos['viewCount'] = recent_videos['statistics'].apply(lambda x: x['viewCount'] if 'viewCount' in x else '')
selected_videos['likeCount'] = recent_videos['statistics'].apply(lambda x: x['likeCount'] if 'likeCount' in x else '')
selected_videos['favoriteCount'] = recent_videos['statistics'].apply(lambda x: x['favoriteCount'] if 'favoriteCount' in x else '')
selected_videos['commentCount'] = recent_videos['statistics'].apply(lambda x: x['commentCount'] if 'commentCount' in x else '')

# Lấy danh sách duy nhất các channelId từ selected_videos
unique_channel_ids = selected_videos['channelId'].unique()

# In danh sách channelIds
print("Unique Channel IDs:")
print(unique_channel_ids)

# Tiếp tục xử lý như trước để lấy thông tin kênh và lưu vào CSV
for channel_id in unique_channel_ids:
    # Check if the channelId already exists in the CSV file
    if not channel_id_exists(csv_file, channel_id):
        # Get channel information
        channel_info = get_channel_info(channel_id)

        # Process channel information as needed
        if channel_info:
            # Extract relevant information
            channel_title = channel_info['snippet']['title']
            channel_description = channel_info['snippet']['description'].replace('\n', ' ')
            subscriber_count = channel_info['statistics']['subscriberCount']

            # Create a DataFrame to store channel information
            channel_data = pd.DataFrame({
                'channelId': [channel_id],
                'channelTitle': [channel_title],
                'channelDescription': [channel_description],
                'subscriberCount': [subscriber_count]
            })

            # Append channel data to the CSV file
            append_channel_data(csv_file, channel_data)
        else:
            print(f"Channel with ID {channel_id} not found.")
    else:
        print(f"Channel with ID {channel_id} already exists in the CSV file.")
