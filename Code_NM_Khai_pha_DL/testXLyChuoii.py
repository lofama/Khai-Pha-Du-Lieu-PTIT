import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

# Dữ liệu mẫu
text_data = [
    ['dong tay promotion', 'đông tây promotion', 'htv', 'tvshow', 'gameshow', '2 ngày 1 đêm', '2 ngay 1 dem', '2 ngày 1 đêm việt nam', '2 ngay 1 dem viet nam', '2 days 1 night', '2N1Đ', 'chương trình thực tế 2022', 'game show mới nhất 2022', 'trường giang', 'truong giang', 'kiều minh tuấn', 'kieu minh tuan', 'cris phan', 'dương lâm', 'lê dương bảo lâm', 'ngô kiến huy', 'ngo kien huy', 'duong lam', 'hieuthuhai', 'le duong bao lam', '2 ngày 1 đêm full', '2 ngày 1 đêm tập 1', '2 ngay 1 dem tap 1', 'tập 1 2 ngày 1 đêm', 'tap 1 2 ngay 1 dem'],
    ['example', 'another example', 'tvshow', 'gameshow', '2 ngày 1 đêm', '2 ngay 1 dem', 'chương trình thực tế 2022'],
]

# Chuyển danh sách thành chuỗi văn bản
text_data = [' '.join(map(str, x)) for x in text_data]

# Sử dụng CountVectorizer
vectorizer = CountVectorizer(binary=True)
X = vectorizer.fit_transform(text_data)

# Tạo DataFrame từ ma trận kết quả
df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())

# Thêm cột mới vào DataFrame
df['word_presence'] = df.apply(lambda row: ', '.join([str(1) if val == 1 else str(0) for val in row]), axis=1)

# In ra kết quả
print(df)

# Lặp qua từng dòng của DataFrame
for index, row in df.iterrows():
    print(f"Example {index + 1}:", end=" ")

    # Lặp qua từng cột (từ) và giá trị tương ứng
    for col in df.columns[:-1]:  # Bỏ qua cột cuối cùng vì đó là cột word_presence
        print(f"{col}: {row[col]}", end=", ")

    # In giá trị của cột word_presence
    print(f"word_presence: {row['word_presence']}")


