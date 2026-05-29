import re
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


def clean_text(text):
    text = str(text).lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


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
