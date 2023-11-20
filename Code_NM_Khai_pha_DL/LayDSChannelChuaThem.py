import pandas as pd

# Đọc dữ liệu từ file CSV hoặc DataFrame của bạn
channel_data = pd.read_csv('ChannelData.csv')
video_data = pd.read_csv('DataVideo.csv')

# Lấy danh sách các ID kênh có trong ChannelData mà không có trong videoData
missing_channel_ids = channel_data[~channel_data['channelId'].isin(video_data['channelId'])]['channelId']
newId = missing_channel_ids.to_list()
# In ra danh sách các ID kênh
print("Các ID kênh không có trong videoData:")
print(newId,len(newId))
