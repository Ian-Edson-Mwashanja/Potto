import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
# 1. Load the engineered dataset
df = pd.read_csv("data/engineered_features.csv")
print("Dataset loaded successfully!")
print("Total records:", len(df))
# 2. Select the features
features = [
    "mean_magnitude",
    "max_magnitude",
    "min_magnitude",
    "std_magnitude",
    "range_magnitude"
]
X = df[features]
y = df["label"]
# 3. Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)
# 4. Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
# 5. Train the model
print("\nTraining Potto AI model...")
model.fit(X_train, y_train)
print("Training completed!")
# 6. Test the model
predictions = model.predict(X_test)
accuracy = accuracy_score(
    y_test,
    predictions
)
print("\nModel Accuracy:")
print(f"{accuracy * 100:.2f}%")
# 7. Save the trained model
model_path = "ai/potto_model.pkl"
joblib.dump(model, model_path)
print("\nAI model saved successfully!")
print("Model location:")
print(model_path)
