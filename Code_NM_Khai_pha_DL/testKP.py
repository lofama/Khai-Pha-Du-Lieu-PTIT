import pandas as pd

# Đọc dữ liệu từ các file CSV
video_data = pd.read_csv('DataVideo.csv')
channel_data = pd.read_csv('ChannelData.csv')
youtube_data_trend = pd.read_csv('DataYoutubeTrending.csv')

# Chuyển cột tags và tags1 thành chuỗi văn bản (nếu chưa phải)
youtube_data_trend['tags'] = youtube_data_trend['tags'].astype(str)
video_data['tags1'] = video_data['tags'].astype(str)

# Tính số từ trong tags1 có trong tags cho mỗi mẫu
video_data['common_words_count'] = video_data.apply(lambda row: sum(word in row['tags'] for word in row['tags1'].split()), axis=1)

# Chọn các cột quan trọng từ video_data
video_data = video_data[['id', 'publishedAt', 'channelId', 'title', 'dimension', 'tags', 'common_words_count', 'viewCount', 'likeCount', 'commentCount']]

# Gộp dữ liệu từ video_data và channel_data bằng cột 'channelId'
merged_data = pd.merge(video_data[['id', 'publishedAt', 'dimension', 'channelId', 'title', 'tags', 'common_words_count', 'viewCount', 'likeCount', 'commentCount']],
                      channel_data[['channelId', 'subscriberCount']],
                      on='channelId',
                      how='left')

# Tính giá trị trung bình cho lượt xem, lượt thích và lượng bình luận
avg_view_count = youtube_data_trend['viewCount'].mean()
avg_like_count = youtube_data_trend['likeCount'].mean()
avg_comment_count = youtube_data_trend['commentCount'].mean()

# Chọn các cột quan trọng từ merged_data
final_data = merged_data[['id', 'publishedAt', 'dimension', 'channelId', 'title', 'tags', 'common_words_count', 'subscriberCount', 'viewCount', 'likeCount', 'commentCount']]

# Đổi tên cột cho dễ hiểu
final_data.columns = ['id', 'publishedAt', 'dimension', 'channelId', 'title', 'tags', 'common_words_count', 'subscriberCount', 'viewCount', 'likeCount', 'commentCount']

# Xử lý giá trị null bằng cách điền giá trị mặc định (ví dụ: 'Unknown' cho các cột chuỗi)
final_data.loc[:, 'publishedAt'] = final_data['publishedAt'].fillna('Unknown')
final_data.loc[:, 'dimension'] = final_data['dimension'].fillna('Unknown')
final_data.loc[:, 'channelId'] = final_data['channelId'].fillna('Unknown')
final_data.loc[:, 'title'] = final_data['title'].fillna('Unknown')
final_data.loc[:, 'tags'] = final_data['tags'].fillna('Unknown')
final_data.loc[:, 'subscriberCount'] = final_data['subscriberCount'].fillna(0)

# Lấy danh sách các giá trị duy nhất từ cột "id" của youtube_data_trend
trending_ids = youtube_data_trend['id'].unique()
final_data = final_data.copy()  # Create a copy of the DataFrame

# Thêm cột "trend" vào final_data
final_data.loc[:, 'trend'] = ((final_data['viewCount'] > avg_view_count) & 
                               (final_data['likeCount'] > avg_like_count) & 
                               (final_data['commentCount'] > avg_comment_count) & 
                               final_data['id'].astype(str).isin(trending_ids)).astype(int)

# Lưu dữ liệu vào file CSV mới
final_data.to_csv('TrainingDataWithTrend.csv', index=False)
