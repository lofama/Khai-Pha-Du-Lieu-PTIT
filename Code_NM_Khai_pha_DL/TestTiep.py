import pandas as pd

# Đường dẫn đến file CSV
file_path = 'ChannelData.csv'

# Đọc dữ liệu từ file CSV vào DataFrame
df = pd.read_csv(file_path)

# Hiển thị thông tin cơ bản của DataFrame trước khi xóa cột
print("Dữ liệu ban đầu:")
print(df)

# Xóa cột cuối cùng
df = df.drop(df.columns[-1], axis=1)

# Hiển thị DataFrame sau khi xóa cột cuối cùng
print("\nDữ liệu sau khi xóa cột cuối cùng:")
print(df)

# Ghi DataFrame mới vào file CSV
df.to_csv(file_path, index=False)
