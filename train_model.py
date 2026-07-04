import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 1. Data Load Karo
print("⏳ Loading data...")
df = pd.read_csv('customer_tickets.csv')

# 2. Train aur Test mein split karo (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(df['ticket_text'], df['department'], test_size=0.2, random_state=42)

# 3. TF-IDF Vectorization (Text ko Numbers mein convert karna)
print("🔄 Converting text to numbers (TF-IDF)...")
# stop_words='english' ka matlab hai ke faltu words (is, am, the) ko ignore kar do
vectorizer = TfidfVectorizer(stop_words='english') 
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 4. Model Training (Naive Bayes algorithm Text Classification ke liye best hota hai)
print("🧠 Training the NLP Model...")
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# 5. Model Evaluation (Test lena)
predictions = model.predict(X_test_vec)
print("\n✅ Model Accuracy:", round(accuracy_score(y_test, predictions) * 100, 2), "%")
print("\n📊 Detailed Report:\n", classification_report(y_test, predictions))

# 6. Model aur Vectorizer ko save karna
joblib.dump(model, 'nlp_model.pkl')
joblib.dump(vectorizer, 'nlp_vectorizer.pkl')
print("💾 Model and Vectorizer saved successfully!")