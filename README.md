# 📧 Phân loại email spam

Hệ thống phát hiện Email Spam sử dụng Machine Learning (TF-IDF + Logistic Regression) kết hợp Rule-based Detection.

## 🚀 Tính năng

* Phân loại Email Spam / Ham
* Hỗ trợ tiếng Anh
* Hỗ trợ tiếng Việt có dấu
* Hỗ trợ tiếng Việt không dấu
* Highlight từ khóa nghi ngờ spam
* Batch Upload CSV
* Triển khai trên Streamlit hoặc Render

---

## 📂 Cấu trúc dự án

```text
project/
│
├── app.py
├── train_model.py
├── email.csv
├── phanloaiemail.pkl
├── tfidf_vectorizer.pkl
├── requirements.txt
├── Procfile
└── .streamlit/
    └── config.toml
```

---

## 📊 Dữ liệu huấn luyện

File dữ liệu:

```text
email.csv
```

Định dạng:

```csv
Category,Message
ham,"Please find the attached report."
spam,"Congratulations! You have won $1000."
ham,"Chào anh, em gửi báo giá."
spam,"Chúc mừng bạn đã trúng thưởng."
```

Giá trị hợp lệ:

* ham
* spam

---

## 🧠 Huấn luyện mô hình

Chạy:

```bash
python train_model.py
```

Sau khi huấn luyện thành công sẽ tạo:

```text
phanloaiemail.pkl
tfidf_vectorizer.pkl
```

---

## 💻 Chạy ứng dụng cục bộ

Cài thư viện:

```bash
pip install -r requirements.txt
```

Khởi động:

```bash
streamlit run app.py
```

Truy cập:

```text
http://localhost:8501
```

---

## ☁️ Deploy lên Render

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

---

## 🔍 Ví dụ Spam

```text
Chúc mừng bạn đã trúng thưởng 100 triệu đồng.
```

```text
Vay tiền nhanh, giải ngân trong 5 phút.
```

```text
Claim your free iPhone now.
```

---

## ✅ Ví dụ Ham

```text
Chào anh, em gửi báo giá sản phẩm.
```

```text
Gửi báo cáo cho tôi trước 5 giờ.
```

```text
Please find the attached report.
```

---

## 🛠 Công nghệ sử dụng

* Python
* Streamlit
* Scikit-learn
* TF-IDF Vectorizer
* Logistic Regression
* Pandas
* Joblib

---

## 👨‍💻 Tác giả

Spam Email Classifier Project
