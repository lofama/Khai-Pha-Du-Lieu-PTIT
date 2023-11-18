import pandas as pd
import csv
import json
# Đọc file CSV
df = pd.read_csv('DataVideo.csv')

# Lấy dữ liệu từ cột "channelTitle"
channel_titles = df['channelTitle'].unique()

# Hiển thị danh sách các giá trị
print(channel_titles)
