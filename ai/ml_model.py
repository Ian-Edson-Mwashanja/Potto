import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
# LOAD DATASET
df = pd.read_csv(
    "data/road_vibration_data.csv"
)
print("POTTO MACHINE LEARNING")
print(f"Total records: {len(df)}")
# SELECT FEATURES
features = [
    "x",
    "y",
    "z",
    "magnitude"
]
X = df[features]
y = df["label"]
# SPLIT DATA
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))
# CREATE MODEL
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
# TRAIN MODEL
print("\nTraining model...")
model.fit(
    X_train,
    y_train
)
print("Training complete!")
# MAKE PREDICTIONS
y_pred = model.predict(X_test)
print("\nPredictions:")
print(y_pred[:10])
# CALCULATE ACCURACY
accuracy = accuracy_score(
    y_test,
    y_pred
)
print(
    f"\nModel accuracy: {accuracy * 100:.2f}%"
)
# CONFUSION MATRIX
ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred
)
import matplotlib.pyplot as plt
plt.title("Potto Road Condition Confusion Matrix")
plt.tight_layout()
plt.show()
# TEST A NEW SENSOR READING
new_reading = pd.DataFrame([
    {
        "x": 2.5,
        "y": -2.0,
        "z": 16.5,
        "magnitude": 16.8
    }
])
prediction = model.predict(
    new_reading[features]
)
print("\nNew sensor reading:")
print(new_reading)
print("\nPotto prediction:")
print(prediction[0])
# PREDICTION CONFIDENCE
probabilities = model.predict_proba(
    new_reading[features]
)
classes = model.classes_
print("\nPrediction probabilities:")
for class_name, probability in zip(
    classes,
    probabilities[0]
):
    print(
        f"{class_name}: {probability * 100:.2f}%"
    )

