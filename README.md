# Spam Email Classifier - Render Deploy

## Files
- `app.py`: Streamlit app
- `requirements.txt`: Python packages
- `Procfile`: start command for Render
- `.streamlit/config.toml`: Streamlit server config
- `email.csv`: small demo dataset

## Render settings
Build Command:
```bash
pip install -r requirements.txt
```

Start Command:
```bash
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

## Use your trained model
Replace or add these files in the same folder:
- `phanloaiemail.pkl`
- `tfidf_vectorizer.pkl`

If these files are missing, the app trains a small demo model from `email.csv` automatically.
