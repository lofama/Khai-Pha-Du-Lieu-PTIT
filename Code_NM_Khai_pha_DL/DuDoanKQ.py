import joblib
import pandas as pd
# Load mô hình đã lưu
model_name = 'Random Forest'  # Chọn mô hình bạn muốn sử dụng ('Logistic Regression', 'Random Forest', hoặc 'Support Vector Machine')
loaded_model_train = joblib.load(f'DataTrainedForTrend/{model_name}_model.pkl')
loaded_model_view = joblib.load(f'DataTrainedForView/{model_name}_model.pkl')
# Chuẩn bị dữ liệu nhập vào cho dự đoán
input_data = {
    'hour': 10,  # Thay đổi các giá trị tương ứng với đối tượng bạn muốn dự đoán
    'day_of_week': 2,
    'month': 8,
    'dimension': 300,
    'subscriberCount': 1000000,
    'viewChannelCount': 5000000,
    'title_count': 5,
    'tags_count': 10
}

input_object = pd.DataFrame([input_data])

# Dự đoán giá trị 'viewTB' cho đối tượng nhập vào
predicted_value_train = loaded_model_train.predict(input_object)[0]
predicted_value_view = loaded_model_view.predict(input_object)[0]
# Hiển thị thông tin về đối tượng và giá trị dự đoán
print("Input Object:")
print(input_object)
print("\nPredicted 'viewTB'(Lượng view dự đoán) Value:", predicted_value_view)
print("\nPredicted 'Train' (1: Yes 0: No)Value:", predicted_value_train)
