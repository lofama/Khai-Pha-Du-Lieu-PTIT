import pandas as pd

# Đọc dữ liệu từ file CSV
df_channel = pd.read_csv('ChannelData.csv')
df_video = pd.read_csv('DataVideo.csv')

# Lấy danh sách unique các channelTitle từ cả hai file
unique_channel_titles_channel = set(df_channel['channelId'].unique())
unique_channel_titles_video = set(df_video['channelId'].unique())

# Tìm những channelTitle không xuất hiện ở cả hai file
unique_channel_titles_only_in_channel = unique_channel_titles_channel - unique_channel_titles_video
unique_channel_titles_only_in_video = unique_channel_titles_video - unique_channel_titles_channel

# In kết quả
print("Channel titles only in ChannelData.csv:", unique_channel_titles_only_in_channel)
print("Channel titles only in DataVideo.csv:", unique_channel_titles_only_in_video)
