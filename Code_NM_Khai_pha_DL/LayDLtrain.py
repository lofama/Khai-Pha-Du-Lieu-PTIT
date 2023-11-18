import pandas as pd

# Đọc dữ liệu từ các file CSV
video_data = pd.read_csv('DataVideo.csv')
channel_data = pd.read_csv('ChannelData.csv')
youtube_data = pd.read_csv('DataYoutubeTrending.csv')

# Chọn các cột quan trọng từ video_data
video_data = video_data[['id', 'publishedAt', 'channelId', 'title', 'duration', 'tags', 'viewCount', 'likeCount', 'commentCount']]

# Gộp dữ liệu từ video_data và channel_data bằng cột 'channelId'
merged_data = pd.merge(video_data, channel_data, on='channelId', how='left')

# Tính giá trị trung bình cho lượt xem, lượt thích và lượng bình luận
avg_view_count = youtube_data['viewCount'].mean()
avg_like_count = youtube_data['likeCount'].mean()
avg_comment_count = youtube_data['commentCount'].mean()

# Chọn các cột quan trọng từ merged_data
final_data = merged_data[['id', 'publishedAt', 'duration', 'channelId', 'title', 'tags', 'subscriberCount', 'viewCount', 'likeCount', 'commentCount']]

# Đổi tên cột cho dễ hiểu
final_data.columns = ['id', 'publishedAt', 'duration', 'channelId', 'title', 'tags', 'subscriberCount', 'viewCount', 'likeCount', 'commentCount']

# Xử lý giá trị null bằng cách điền giá trị mặc định (ví dụ: 'Unknown' cho các cột chuỗi)
final_data['publishedAt'].fillna('Unknown', inplace=True)
final_data['duration'].fillna('Unknown', inplace=True)
final_data['channelId'].fillna('Unknown', inplace=True)
final_data['title'].fillna('Unknown', inplace=True)
final_data['tags'].fillna('Unknown', inplace=True)
final_data['subscriberCount'].fillna(0, inplace=True)
# Lấy danh sách các giá trị duy nhất từ cột "id" của youtube_data
trending_ids = youtube_data['id'].unique()

# Thêm cột "trend" vào final_data
final_data['trend'] = ((final_data['viewCount'] > avg_view_count) | 
                       (final_data['likeCount'] > avg_like_count) | 
                       (final_data['commentCount'] > avg_comment_count)|final_data['id'].isin(trending_ids)).astype(int)

# Lưu dữ liệu vào file CSV mới
final_data.to_csv('TrainingDataWithTrend.csv', index=False)

