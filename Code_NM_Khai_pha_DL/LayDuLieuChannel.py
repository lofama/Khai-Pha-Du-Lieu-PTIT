import os
import requests
import json
import pandas as pd

# Thay thế 'YOUR_API_KEY' bằng khóa API của bạn
API_KEY = 'AIzaSyCsBnmdjr2SDnjuL5ZTIp-6UbOAQ4aNt3A'

# Function to get channel information by channelId
def get_channel_info(channel_id):
    url = f'https://www.googleapis.com/youtube/v3/channels?key={API_KEY}&part=snippet,statistics&id={channel_id}'
    response = requests.get(url)
    data = json.loads(response.text)
    print(data)
    return data['items'][0] if 'items' in data else None

# Function to check if a channelId already exists in the CSV file
def channel_id_exists(csv_file, channel_id):
   # Kiểm tra xem file CSV đã tồn tại hay chưa
    if os.path.exists(csv_file):
        # Đọc file CSV nếu tồn tại
        df = pd.read_csv(csv_file)
    else:
        # Nếu không tồn tại, tạo DataFrame mới với các cột đã cho
        df = pd.DataFrame(columns=['channelId', 'title', 'description', 'subscriberCount'])
        df.to_csv(csv_file, header=True, index=False)
        return False

    # Kiểm tra xem channelId đã tồn tại trong DataFrame hay chưa
    return channel_id in df['channelId'].values

# Function to append channel data to the CSV file
def append_channel_data(csv_file, channel_data):
    channel_data.to_csv(csv_file, mode='a', header=False, index=False)
    print(f"Channel information for {channel_data['channelTitle'].iloc[0]} saved successfully.")

# Example usage
csv_file = 'ChannelData.csv'
# Lấy danh sách duy nhất các channelId từ selected_videos
# unique_channel_ids =  pd.read_csv('DataYoutubeTrending.csv')['channelId'].unique()
unique_channel_ids={'UCvx0yETx4Mg0Si_YifV3-2g', 'UCDt2sv8-Uw3ziTy2G7Bjktw', 'UCA_23dkEYToAc37hjSsCnXA', 'UCvjOPaJZjDkgSkXsfAchSwQ', 'UC3IZKseVpdzPSBaWxBxundA', 'UC7XYZvX1jEKdLsq_bZs2gjQ', 'UCLa90xY6l4sEY1sC3tlwGGA', 'UCZRWf-SUOu4c8FSq2ezH-Zw', 'UCKkYlIkbgikL76LrddIM98w', 'UChGncdgzOKmp5XQTnQa2h4w', 'UC89u8T2JjgjAo1G37dXLLWw', 'UC0IpGYsi1KVorZ7QVCHfdag', 'UCAzZdEu3MjJ7kdJD-u2083Q', 'UC475tLo6Mop8IYXgvdnJy8w', 'UCxE_qxE-rBRn2mePLwJulIw', 'UCfDrdfgDyeF_h3Y8klV0e0w', 'UCAhfSPCb_HzvHSI54YCZ6GA', 'UC6UrwtJjV4xPxxZo-ZEpQYA', 'UCgeQezjQQi43YaBFWD5vUyQ', 'UC8ahGDcou5XFUEVf4ID69vQ', 'UCJSagsGX4aEwIejLp_9NkbA', 'UCYd8eNMptkrGQs5F1JFHgMA', 'UCD7jwWWYc8OsLBi_q64DTnA', 'UCbTAemQCm6Rud3HD0k30Qow', 'UC2k3OPgIJWjp63Y2hrxdHHA', 'UCPhHBEtG6dVZ5fJKoNArcJw', 'UCZxUVZjMMx_xIjRuHyi4tUg', 'UC5fsYtWjjzy8D13cn4UKVMQ', 'UC2BEmluQX1foBrR3oLMiB_g', 'UCsluIbpgt14y6KUcwqCxXbg', 'UCzgN9ZHWGlyk23LysJskf9Q', 'UCjoAIOyTWjGjP_Q-qw3jkhQ', 'UCTAacyv5T4cSus1W4D6eBfA', 'UCiWyQp2HgKX2-WQUq11V8FA'}
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