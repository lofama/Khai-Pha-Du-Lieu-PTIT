import pandas as pd

# Đọc dữ liệu từ file CSV
df = pd.read_csv('TrainingDataWithTrend.csv')

# Kiểm tra giá trị null và in ra số lượng giá trị null trong từng cột
null_counts = df.isnull().sum()

# In ra các cột có giá trị null và số lượng giá trị null tương ứng
for column, count in null_counts.items():
    if count > 0:
        print(f'{column}: {count} giá trị null')

# Nếu bạn muốn hiển thị toàn bộ dòng có giá trị null, sử dụng df[df.isnull().any(axis=1)]
# Ví dụ: df[df.isnull().any(axis=1)].head() để in ra 5 dòng đầu tiên có giá trị null
