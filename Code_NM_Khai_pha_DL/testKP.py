import pandas as pd

# Đọc dữ liệu từ file CSV
final_data = pd.read_csv('DataVideo.csv')

# Xem giá trị isnull của mỗi cột
null_values = final_data.isnull().sum()

# Hiển thị kết quả
print(null_values)
