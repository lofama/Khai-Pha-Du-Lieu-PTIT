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
        df = pd.DataFrame(columns=['channelId', 'channelTitle', 'channelDescription', 'subscriberCount', 'viewChannelCount'])
        df.to_csv(csv_file, header=True, index=False)
        return False

    # Kiểm tra xem channelId đã tồn tại trong DataFrame hay chưa
    return channel_id in df['channelId'].values

# Function to append channel data to the CSV file
def append_channel_data(csv_file, channel_data):
    channel_data.to_csv(csv_file, mode='a', header=False, index=False)
    print(f"Channel information for {channel_data['channelTitle'].iloc[0]} saved successfully.")

# Example usage
csv_file = 'Te.csv'
# Lấy danh sách các channelId từ YouTube
# queries = [
#     'health', 'fitness', 'wellness', 'beauty', 'skincare', 'nutrition', 'exercise',
#     'education', 'learning', 'personal development', 'self-improvement', 'skills development', 'knowledge',
#     'art', 'culture', 'creativity', 'literature', 'music', 'film', 'performance',
#     'family', 'relationships', 'parenting', 'marriage', 'communication', 'love',
#     'business', 'career', 'entrepreneurship', 'leadership', 'success', 'innovation',
#     'entertainment', 'relaxation', 'hobbies', 'games', 'humor', 'movies', 'travel',
#     'science', 'technology', 'innovation', 'discovery', 'research', 'gadgets',
#     'psychology', 'mental health', 'mindfulness', 'meditation', 'happiness', 'stress management',
#     'social issues', 'activism', 'equality', 'diversity', 'peace', 'community',
#     'sports', 'outdoor activities', 'adventure', 'fitness sports', 'recreational activities'
# ]
queries = ['fitness', 'health', 'education', 'music', 'travel', 'science', 'art', 'fashion', 'food', 'film', 'games', 'sports', 'love', 'kids', 'beauty', 'news', 'mobile devices', 'technology', 'e-commerce', 'lifestyle', 'accessories', 'design', 'software', 'cars', 'electronics', 'home appliances', 'toys', 'office equipment', 'audio equipment', 'entertainment equipment', 'wearable devices', 'medical equipment', 'navigation devices', 'security equipment', 'peripheral devices', 'networking equipment', 'storage devices', 'clocks', 'measuring equipment', 'electrical equipment', 'sanitary equipment', 'cooking equipment', 'gardening equipment', 'pet equipment', 'sports equipment', 'healthcare equipment', 'beauty equipment', 'communication equipment', 'beverage equipment', 'jewelry equipment']
# Số lượng channelId bạn muốn lấy cho mỗi từ khóa
num_channels_per_keyword = 10

# Hàm để lấy danh sách các channelId ngẫu nhiên
def get_random_channel_ids(api_key, queries, num_channels_per_query=10):
    all_channel_ids = []

    for query in queries:
        url = f'https://www.googleapis.com/youtube/v3/search?key={api_key}&part=id&type=channel&q={query}&maxResults={num_channels_per_query}&regionCode=VN'
        response = requests.get(url)
        data = json.loads(response.text)

        # Lấy `channelId` từ kết quả tìm kiếm
        if 'items' in data:
            channel_ids = [item['id']['channelId'] for item in data['items']]
            all_channel_ids.extend(channel_ids)

    return all_channel_ids
# Lấy danh sách duy nhất các channelId từ selected_videos
# unique_channel_ids =  pd.read_csv('DataYoutubeTrending.csv')['channelId'].unique()
# unique_channel_ids={'UCvx0yETx4Mg0Si_YifV3-2g', 'UCDt2sv8-Uw3ziTy2G7Bjktw', 'UCA_23dkEYToAc37hjSsCnXA', 'UCvjOPaJZjDkgSkXsfAchSwQ', 'UC3IZKseVpdzPSBaWxBxundA', 'UC7XYZvX1jEKdLsq_bZs2gjQ', 'UCLa90xY6l4sEY1sC3tlwGGA', 'UCZRWf-SUOu4c8FSq2ezH-Zw', 'UCKkYlIkbgikL76LrddIM98w', 'UChGncdgzOKmp5XQTnQa2h4w', 'UC89u8T2JjgjAo1G37dXLLWw', 'UC0IpGYsi1KVorZ7QVCHfdag', 'UCAzZdEu3MjJ7kdJD-u2083Q', 'UC475tLo6Mop8IYXgvdnJy8w', 'UCxE_qxE-rBRn2mePLwJulIw', 'UCfDrdfgDyeF_h3Y8klV0e0w', 'UCAhfSPCb_HzvHSI54YCZ6GA', 'UC6UrwtJjV4xPxxZo-ZEpQYA', 'UCgeQezjQQi43YaBFWD5vUyQ', 'UC8ahGDcou5XFUEVf4ID69vQ', 'UCJSagsGX4aEwIejLp_9NkbA', 'UCYd8eNMptkrGQs5F1JFHgMA', 'UCD7jwWWYc8OsLBi_q64DTnA', 'UCbTAemQCm6Rud3HD0k30Qow', 'UC2k3OPgIJWjp63Y2hrxdHHA', 'UCPhHBEtG6dVZ5fJKoNArcJw', 'UCZxUVZjMMx_xIjRuHyi4tUg', 'UC5fsYtWjjzy8D13cn4UKVMQ', 'UC2BEmluQX1foBrR3oLMiB_g', 'UCsluIbpgt14y6KUcwqCxXbg', 'UCzgN9ZHWGlyk23LysJskf9Q', 'UCjoAIOyTWjGjP_Q-qw3jkhQ', 'UCTAacyv5T4cSus1W4D6eBfA', 'UCiWyQp2HgKX2-WQUq11V8FA'}
unique_channel_ids = get_random_channel_ids(API_KEY,queries,num_channels_per_query=5)
newChannelId=[]
# Tiếp tục xử lý như trước để lấy thông tin kênh và lưu vào CSV
for channel_id in unique_channel_ids:
    # Check if the channelId already exists in the CSV file
    if not channel_id_exists(csv_file, channel_id):
        # Get channel information
        channel_info = get_channel_info(channel_id)

        # Process channel information as needed
        if channel_info:
            snippet = channel_info.get('snippet', {})
            statistics = channel_info.get('statistics', {})
            
            # Extract relevant information
            channel_title = snippet.get('title', '')
            channel_description = snippet.get('description', '').replace('\n', ' ')
            subscriber_count = statistics.get('subscriberCount', 0)
            view_count = statistics.get('viewChannelCount', 0)
            
            # Create a DataFrame to store channel information
            channel_data = pd.DataFrame({
                'channelId': [channel_id],
                'channelTitle': [channel_title],
                'channelDescription': [channel_description],
                'subscriberCount': [subscriber_count],
                'viewChannelCount': [view_count],
            })

            # Append channel data to the CSV file
            append_channel_data(csv_file, channel_data)
        else:
            print(f"Channel with ID {channel_id} not found.")
    else:
        print(f"Channel with ID {channel_id} already exists in the CSV file.")

print(newChannelId)