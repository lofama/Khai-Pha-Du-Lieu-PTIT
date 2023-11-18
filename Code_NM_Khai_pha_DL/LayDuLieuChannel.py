import os
import requests
import json
import pandas as pd

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

# Example usage
channel_id = 'UCFMEYTv6N64hIL9FlQ_hxBw'  # Replace with your channel ID
csv_file = 'ChannelData.csv'

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
