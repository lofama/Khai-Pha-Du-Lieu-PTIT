import pandas as pd

# Đọc dữ liệu từ file CSV
data = pd.read_csv('DataYoutubeTrending.csv')
data1 = pd.read_csv('TrainingDataWithTrend.csv')

# Chuyển cột tags và tags1 thành chuỗi văn bản (nếu chưa phải)
data['tags'] = data['tags'].astype(str)
data1['tags1'] = data1['tags'].astype(str)

# Tính số từ trong tags1 có trong tags cho mỗi mẫu
data1['common_words_count'] = data1.apply(lambda row: sum(word in row['tags'] for word in row['tags1'].split()), axis=1)

# In ra kết quả
print(data1[['tags1', 'common_words_count']])
