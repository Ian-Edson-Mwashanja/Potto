import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)
import matplotlib.pyplot as plt
# 1. Load engineered features
df = pd.read_csv("data/engineered_features.csv")
print("Dataset loaded successfully!")
print("Number of records:", len(df))
print("\nFirst 5 records:")
print(df.head())
# 2. Select features
features = [
    "mean_magnitude",
    "max_magnitude",
    "min_magnitude",
    "std_magnitude",
    "range_magnitude"
]
X = df[features]
y = df["label"]
# 3. Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)
print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))
# 4. Create Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
# 5. Train the model
print("\nTraining model...")
model.fit(X_train, y_train)
print("Training completed!")
# 6. Make predictions
y_pred = model.predict(X_test)
# 7. Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("MODEL ACCURACY")
print(f"Accuracy: {accuracy * 100:.2f}%")
# 8. Classification report
print("CLASSIFICATION REPORT")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)
# 9. Confusion matrix
print("CONFUSION MATRIX")
cm = confusion_matrix(y_test, y_pred)
print(cm)
# 10. Display confusion matrix
display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=model.classes_
)
display.plot(
    xticks_rotation=45
)
plt.title("Potto Road Condition Classifier")
plt.tight_layout()
plt.show()