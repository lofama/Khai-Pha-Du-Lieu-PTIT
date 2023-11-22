import pandas as pd
channel_data = pd.read_csv('ChannelData.csv')
id = channel_data['channelId'].to_list()
print(id)