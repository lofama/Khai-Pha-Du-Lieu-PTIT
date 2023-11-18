import requests
import json
import pandas as pd
from datetime import datetime, timedelta

# Thay thế 'YOUR_API_KEY' bằng khóa API của bạn
API_KEY = 'AIzaSyAIauebrmC4h8cXkY8a2UHsKHmhufHeFOs'
# Số lượng video bạn muốn lấy
desired_video_count = 1

# Thời điểm hiện tại
current_time = datetime.utcnow()

# Lấy thời điểm 7 ngày trước
start_time = current_time - timedelta(days=30)
print(start_time)
# Định dạng thời gian theo ISO 8601
published_after = start_time.isoformat() + "Z"  # Z indicates UTC time
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
    url = f'https://www.googleapis.com/youtube/v3/videos?key={API_KEY}&part=snippet,contentDetails,statistics&chart=mostPopular&regionCode=VN&maxResults=100&publishedAfter={published_after}&publishedBefore={published_before}'

    if next_page_token:
        url += f'&pageToken={next_page_token}'

    # Gửi yêu cầu API và chuyển đổi dữ liệu JSON
    response = requests.get(url)
    data = json.loads(response.text)
    print(data)
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

# Chọn các cột bạn quan trọng
selected_columns = ['id']

# Tạo DataFrame mới chỉ chứa các cột bạn quan tâm
selected_videos = videos[selected_columns].copy()

# Truy cập 'publishedAt' trong 'snippet'
selected_videos['publishedAt'] = videos['snippet'].apply(lambda x: x['publishedAt'] if 'publishedAt' in x else '')
selected_videos['channelId'] = videos['snippet'].apply(lambda x: x['channelId'] if 'channelId' in x else '')
selected_videos['title'] = videos['snippet'].apply(lambda x: x['title'] if 'title' in x else '')
selected_videos['channelTitle'] = videos['snippet'].apply(lambda x: x['channelTitle'] if 'channelTitle' in x else '')
selected_videos['tags'] = videos['snippet'].apply(lambda x: x['tags'] if 'tags' in x else '')
selected_videos['duration'] = videos['contentDetails'].apply(lambda x: x['duration'] if 'duration' in x else '')
selected_videos['dimension'] = videos['contentDetails'].apply(lambda x: x['dimension'] if 'dimension' in x else '')
selected_videos['definition'] = videos['contentDetails'].apply(lambda x: x['definition'] if 'definition' in x else '')
selected_videos['caption'] = videos['contentDetails'].apply(lambda x: x['caption'] if 'caption' in x else '')
selected_videos['licensedContent'] = videos['contentDetails'].apply(lambda x: x['licensedContent'] if 'licensedContent' in x else '')
selected_videos['contentRating'] = videos['contentDetails'].apply(lambda x: x['contentRating'] if 'contentRating' in x else '')
selected_videos['projection'] = videos['contentDetails'].apply(lambda x: x['projection'] if 'projection' in x else '')
selected_videos['viewCount'] = videos['statistics'].apply(lambda x: x['viewCount'] if 'viewCount' in x else '')
selected_videos['likeCount'] = videos['statistics'].apply(lambda x: x['likeCount'] if 'likeCount' in x else '')
selected_videos['favoriteCount'] = videos['statistics'].apply(lambda x: x['favoriteCount'] if 'favoriteCount' in x else '')
selected_videos['commentCount'] = videos['statistics'].apply(lambda x: x['commentCount'] if 'commentCount' in x else '')

# In ra DataFrame mới
print(selected_videos)

# Lưu DataFrame vào CSV
selected_videos.to_csv('DataYoutubeTrending.csv', index=False)
