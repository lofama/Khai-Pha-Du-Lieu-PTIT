import pandas as pd
import joblib

def preprocess_input_data(input_data):
    # Thực hiện các bước tiền xử lý tương tự như khi huấn luyện mô hình
    # Bạn cần xác định các bước tiền xử lý cần thiết cho dữ liệu đầu vào của mình
    # ở đây để có thể chạy mô hình một cách đúng đắn.

    # Ví dụ: Chuyển đổi cột ngày tháng giờ
    input_data['publishedAt'] = pd.to_datetime(input_data['publishedAt'])
    input_data['hour'] = input_data['publishedAt'].dt.hour
    input_data['day_of_week'] = input_data['publishedAt'].dt.dayofweek
    input_data['month'] = input_data['publishedAt'].dt.month

    # ... (Các bước tiền xử lý dữ liệu khác)
    input_data['title_count'] = input_data['title'].apply(lambda x: len(x.split()))
    input_data['tags_count'] = input_data['tags'].apply(lambda x: len(x.split(',')))

    # Chọn các đặc trưng cần thiết
    selected_features = ['hour', 'day_of_week', 'month', 'dimension', 'subscriberCount', 'title_count', 'tags_count']
    input_data_processed = input_data[selected_features]

    return input_data_processed

def main():
    # Đọc dữ liệu đầu vào từ người dùng
    date_published = input("Nhập ngày tháng giờ (yyyy-mm-dd HH:MM:SS): ")
    title = input("Nhập tiêu đề: ")
    tags = input("Nhập tags (phân cách bởi dấu phẩy): ")

    # Tạo DataFrame từ dữ liệu đầu vào
    input_data = pd.DataFrame({
        'publishedAt': [date_published],
        'title': [title],
        'tags': [tags],
        'dimension': 60,
        'subscriberCount': 10000000
        # Thêm các cột khác cần thiết tương tự như trong quá trình huấn luyện
    })

    # Tiền xử lý dữ liệu đầu vào
    input_data_processed = preprocess_input_data(input_data)

    # Load mô hình đã được huấn luyện
    model = joblib.load('DataTrained/Logistic Regression_model.pkl')  # Đặt tên file mô hình đã được lưu

    # Dự đoán kết quả
    prediction = model.predict(input_data_processed)

    # In kết quả dự đoán
    print(f"Dự đoán kết quả: {prediction}")

if __name__ == "__main__":
    main()
