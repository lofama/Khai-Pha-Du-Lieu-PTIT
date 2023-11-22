import pandas as pd
import numpy as np
# Đọc dữ liệu từ các file CSV
video_data = pd.read_csv('DataVideo.csv')
channel_data = pd.read_csv('ChannelData.csv')
youtube_data = pd.read_csv('DataYoutubeTrending.csv')
# Đọc dữ liệu từ file CSV
data = pd.read_csv('DataYoutubeTrending.csv')
data1 = pd.read_csv('TrainingDataWithTrend.csv')

# Chuyển cột tags và tags1 thành chuỗi văn bản (nếu chưa phải)
data['tags'] = data['tags'].astype(str)
data1['tags1'] = data1['tags'].astype(str)
data['title'] = data['title'].astype(str)
data1['title1'] = data1['title'].astype(str)
# Tính số từ trong tags1 có trong tags cho mỗi mẫu
data1['common_words_count'] = data1.apply(lambda row: sum(word in row['tags'] for word in row['tags1'].split()), axis=1)
data1['common_words_count_title'] = data1.apply(lambda row: sum(word in row['title'] for word in row['title1'].split()), axis=1)
# Chọn các cột quan trọng từ video_data
video_data = video_data[['id', 'publishedAt', 'channelId', 'title', 'dimension', 'tags', 'viewCount', 'likeCount', 'commentCount']]

# Gộp dữ liệu từ video_data và channel_data bằng cột 'channelId'
merged_data = pd.merge(video_data[['id', 'publishedAt', 'dimension', 'channelId', 'title', 'tags', 'viewCount', 'likeCount', 'commentCount']],
                      channel_data[['channelId', 'subscriberCount','viewChannelCount']],
                      on='channelId',
                      how='left')
print(merged_data.columns)
# Tính giá trị trung bình cho lượt xem, lượt thích và lượng bình luận
avg_view_count = youtube_data['viewCount'].mean()
avg_like_count = youtube_data['likeCount'].mean()
avg_comment_count = youtube_data['commentCount'].mean()
print(avg_view_count,avg_like_count,avg_comment_count)
# Chọn các cột quan trọng từ merged_data
final_data = merged_data[['id', 'publishedAt', 'dimension', 'channelId', 'title', 'tags', 'subscriberCount','viewChannelCount', 'viewCount', 'likeCount', 'commentCount']]
# Đổi tên cột cho dễ hiểu
final_data.columns = ['id', 'publishedAt', 'dimension', 'channelId', 'title', 'tags', 'subscriberCount','viewChannelCount', 'viewCount', 'likeCount', 'commentCount']

# Xử lý giá trị null bằng cách điền giá trị mặc định (ví dụ: 'Unknown' cho các cột chuỗi)
final_data.loc[:, 'publishedAt'] = final_data['publishedAt'].fillna('Unknown')
final_data.loc[:, 'dimension'] = final_data['dimension'].fillna('Unknown')
final_data.loc[:, 'channelId'] = final_data['channelId'].fillna('Unknown')
final_data.loc[:, 'title'] = final_data['title'].fillna('Unknown')
final_data.loc[:, 'tags'] = final_data['tags'].fillna('Unknown')
final_data.loc[:, 'subscriberCount'] = final_data['subscriberCount'].fillna(0)
final_data.loc[:, 'viewChannelCount'] = final_data['viewChannelCount'].fillna(0)
# Lấy danh sách các giá trị duy nhất từ cột "id" của youtube_data
trending_ids = youtube_data['id'].unique()
final_data = final_data.copy()  # Create a copy of the DataFrame
# Thêm cột "common_words_count" vào DataFrame gốc
final_data.loc[:,'tags_count'] = data1['common_words_count'].fillna(0)
final_data.loc[:,'title_count'] = data1['common_words_count_title'].fillna(0)
# Thêm cột "trend" vào final_data
final_data['trend'] = np.where(
    (
        (final_data['viewCount'] > avg_view_count) | 
        (final_data['likeCount'] > avg_like_count) & 
        (final_data['commentCount'] > avg_comment_count) | 
        final_data['id'].astype(str).isin(trending_ids)
    ),
    1,  # Gán 1 nếu điều kiện đúng
    0   # Gán 0 nếu điều kiện sai
)
# Lưu dữ liệu vào file CSV mới
final_data.to_csv('TrainingDataWithTrend.csv', index=False)