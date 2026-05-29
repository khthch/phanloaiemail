import re
import unicodedata
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


def remove_vietnamese_accents(text):
    text = str(text)
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = text.replace("đ", "d").replace("Đ", "D")
    return text


def clean_text(text):
    text = str(text).lower()
    text = remove_vietnamese_accents(text)
    text = re.sub(r"http\S+|www\S+", " link ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


df = pd.read_csv("email.csv", encoding="utf-8")

df["Category"] = df["Category"].astype(str).str.lower().str.strip()
df["Message"] = df["Message"].astype(str)

df["Label"] = df["Category"].map({
    "ham": 0,
    "spam": 1
})

df = df.dropna(subset=["Label"])
df["CleanMessage"] = df["Message"].apply(clean_text)

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    max_features=8000
)

X = vectorizer.fit_transform(df["CleanMessage"])
y = df["Label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

joblib.dump(model, "phanloaiemail.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

print("Đã lưu model thành công.")