import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import joblib
# Đọc dữ liệu từ file CSV
data = pd.read_csv('TrainingDataWithTrend.csv')

# Bước 1: Chuyển đổi dữ liệu thời gian
data['publishedAt'] = pd.to_datetime(data['publishedAt'])
data['hour'] = data['publishedAt'].dt.hour
data['day_of_week'] = data['publishedAt'].dt.dayofweek
data['month'] = data['publishedAt'].dt.month

# Bước 2: Chuyển đổi dữ liệu chuỗi
text_features = ['title', 'tags']
text_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='')),
    ('tfidf', TfidfVectorizer())
])
# Bước 3: Xử lý dữ liệu về thời lượng
data['dimension'] = data['dimension'].apply(lambda x: pd.Timedelta(x).seconds)

# Bước 4: Chuẩn hóa dữ liệu số
numeric_features = ['dimension', 'subscriberCount']
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

# Bước 5: Xử lý giá trị null (nếu còn)
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('text', text_transformer, text_features)
    ])

# Bước 6: Chọn các đặc trưng cần thiết
selected_features = ['hour', 'day_of_week', 'month', 'dimension', 'subscriberCount', 'title_count', 'tags_count']
X = data[selected_features]
y = data['trend']

# Bước 7: Phân chia dữ liệu
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Bước 8: Chọn mô hình học máy
models = {
    'Logistic Regression': LogisticRegression(),
    'Random Forest': RandomForestClassifier(),
    'Support Vector Machine': SVC()
}

# Bước 9 và Bước 10: Huấn luyện và đánh giá từng mô hình
results = {}

for model_name, model in models.items():
     # Huấn luyện mô hình
    for i in range(10):
        model.fit(X_train, y_train)
    # Đánh giá mô hình
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    classification_report_result = classification_report(y_test, y_pred)

    # Lưu kết quả vào dictionary
    results[model_name] = {
        'model': model,
        'accuracy': accuracy,
        'classification_report': classification_report_result
    }

    # Lưu mô hình vào file
    model_filename = f'DataTrained/{model_name}_model.pkl'
    joblib.dump(model, model_filename)

# In kết quả
for model_name, result in results.items():
    print(f'{model_name} Results:')
    print(f'Accuracy: {result["accuracy"]}')
    print('Classification Report:')
    print(result['classification_report'])
    print('\n')