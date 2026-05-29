import re
<<<<<<< HEAD
import unicodedata
import streamlit as st
import pandas as pd
import joblib


def remove_vietnamese_accents(text):
    text = str(text)
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = text.replace("đ", "d").replace("Đ", "D")
    return text
=======
import string
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = Path("phanloaiemail.pkl")
VECTORIZER_PATH = Path("tfidf_vectorizer.pkl")
DATA_PATH = Path("email.csv")
>>>>>>> f79e9b81953cf9af3acd1ea2db8a0803b48bc95a


def clean_text(text):
    text = str(text).lower()
<<<<<<< HEAD
    text = remove_vietnamese_accents(text)
    text = re.sub(r"http\S+|www\S+", " link ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
=======
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    text = re.sub(r"\d+", " ", text)
>>>>>>> f79e9b81953cf9af3acd1ea2db8a0803b48bc95a
    text = re.sub(r"\s+", " ", text).strip()
    return text


<<<<<<< HEAD
def highlight_keywords(text, keywords):
    highlighted_text = text

    for keyword in keywords:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        highlighted_text = pattern.sub(
            lambda m: (
                f"<mark style='background:red;color:white;"
                f"padding:2px;border-radius:3px'>{m.group(0)}</mark>"
            ),
            highlighted_text
        )

    return highlighted_text


model = joblib.load("phanloaiemail.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

st.set_page_config(
    page_title="Spam Email Classifier",
    page_icon="📧",
    layout="wide"
)

st.title("📧 Phân loại email spam")
st.write("Hỗ trợ tiếng Anh, tiếng Việt có dấu và tiếng Việt không dấu.")

tab1, tab2 = st.tabs(["📨 Test Email", "📁 Batch Upload"])

spam_keywords = [
    "free", "click", "win", "offer", "prize", "claim",
    "reward", "money", "urgent", "gift", "cash",

    "miễn phí", "trúng thưởng", "nhận quà", "vay tiền",
    "giải ngân", "xác minh", "khuyến mãi", "bấm vào",
    "nhấn vào", "tài khoản", "sắp bị khóa", "khóa tài khoản",

    "mien phi", "trung thuong", "nhan qua", "vay tien",
    "giai ngan", "xac minh", "khuyen mai", "bam vao",
    "nhan vao", "tai khoan", "sap bi khoa", "khoa tai khoan"
]

rule_spam_keywords = [
    "free", "click", "claim", "prize", "reward",
    "mien phi", "trung thuong", "nhan qua", "vay tien",
    "giai ngan", "xac minh", "khuyen mai", "tai khoan",
    "sap bi khoa", "khoa tai khoan"
]


with tab1:
    st.subheader("Test Email Realtime")

    review = st.text_area("✍️ Nhập nội dung email:", height=150)

    if st.button("🚀 Phân loại"):
        if review.strip():
            clean_review = clean_text(review)
            review_vec = vectorizer.transform([clean_review])

            proba = model.predict_proba(review_vec)[0]
            ham_prob = proba[0]
            spam_prob = proba[1]

            rule_detected = any(k in clean_review for k in rule_spam_keywords)
            threshold = 0.70

            st.write("### 🔎 Kết quả:")

            if rule_detected:
                st.error(f"💀 Spam Detected! (Rule-based + ML: {spam_prob*100:.2f}%)")
            elif spam_prob >= threshold:
                st.error(f"💀 Spam Detected! (Confidence: {spam_prob*100:.2f}%)")
            else:
                st.success(f"✅ Safe (Ham) (Confidence: {ham_prob*100:.2f}%)")

            highlighted = highlight_keywords(review, spam_keywords)

            st.markdown(
                f"### 📌 Highlighted Email\n\n{highlighted}",
                unsafe_allow_html=True
            )

            with st.expander("Xem text sau xử lý"):
                st.write(clean_review)
                st.write(f"Ham probability: {ham_prob:.4f}")
                st.write(f"Spam probability: {spam_prob:.4f}")
                st.write(f"Rule detected: {rule_detected}")

        else:
            st.warning("⚠️ Vui lòng nhập nội dung email!")


with tab2:
    st.subheader("Batch Upload CSV")

    uploaded_file = st.file_uploader("Upload file CSV có cột Message", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, encoding="utf-8")

        if "Message" not in df.columns:
            st.error("File CSV phải có cột Message")
        else:
            df["CleanMessage"] = df["Message"].astype(str).apply(clean_text)
            X_batch = vectorizer.transform(df["CleanMessage"])

            spam_probs = model.predict_proba(X_batch)[:, 1]

            df["Spam_Probability"] = spam_probs
            df["Rule_Detected"] = df["CleanMessage"].apply(
                lambda x: any(k in x for k in rule_spam_keywords)
            )

            df["Prediction"] = [
                "spam" if rule or prob >= 0.70 else "ham"
                for prob, rule in zip(df["Spam_Probability"], df["Rule_Detected"])
            ]

            st.dataframe(df)
=======
def normalize_label(value):
    value = str(value).strip().lower()
    if value in {"spam", "1", "true"}:
        return 1
    return 0


@st.cache_resource
def load_or_train_model():
    if MODEL_PATH.exists() and VECTORIZER_PATH.exists():
        return joblib.load(MODEL_PATH), joblib.load(VECTORIZER_PATH)

    if not DATA_PATH.exists():
        raise FileNotFoundError("Thiếu file email.csv hoặc file model .pkl")

    df = pd.read_csv(DATA_PATH).dropna(subset=["Category", "Message"])
    df["Message"] = df["Message"].apply(clean_text)
    y = df["Category"].apply(normalize_label)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["Message"])

    model = LogisticRegression(class_weight="balanced", max_iter=1000)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    return model, vectorizer


st.set_page_config(page_title="Spam Email Classifier", page_icon="🚨", layout="centered")

st.title("🚨 Spam Email Classifier")
st.caption("Demo phân loại email Spam/Ham bằng TF-IDF + Logistic Regression")

try:
    model, vectorizer = load_or_train_model()
except Exception as exc:
    st.error(f"Không load/train được model: {exc}")
    st.stop()

tab1, tab2 = st.tabs(["📝 Test Email", "📂 Batch CSV"])

with tab1:
    message = st.text_area("Nhập nội dung email:", height=180)

    if st.button("Phân loại"):
        if not message.strip():
            st.warning("Vui lòng nhập nội dung email.")
        else:
            cleaned = clean_text(message)
            vec = vectorizer.transform([cleaned])
            pred = model.predict(vec)[0]

            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(vec)[0]
                confidence = max(proba) * 100
            else:
                confidence = None

            if pred == 1:
                st.error(f"SPAM" + (f" - độ tin cậy {confidence:.2f}%" if confidence else ""))
            else:
                st.success(f"HAM / Không spam" + (f" - độ tin cậy {confidence:.2f}%" if confidence else ""))

with tab2:
    st.write("Upload file CSV có cột `Message`. Nếu có cột `Category`, app vẫn giữ lại để đối chiếu.")
    uploaded = st.file_uploader("Chọn file CSV", type=["csv"])

    if uploaded is not None:
        data = pd.read_csv(uploaded)
        if "Message" not in data.columns:
            st.error("File CSV phải có cột Message")
        else:
            messages = data["Message"].fillna("").apply(clean_text)
            vec = vectorizer.transform(messages)
            pred = model.predict(vec)
            data["Prediction"] = ["Spam" if p == 1 else "Ham" for p in pred]
            if hasattr(model, "predict_proba"):
                data["Confidence"] = model.predict_proba(vec).max(axis=1)
            st.dataframe(data, use_container_width=True)
            st.download_button(
                "Tải kết quả CSV",
                data.to_csv(index=False).encode("utf-8"),
                file_name="spam_predictions.csv",
                mime="text/csv",
            )
>>>>>>> f79e9b81953cf9af3acd1ea2db8a0803b48bc95a
