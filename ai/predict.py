import joblib
import pandas as pd
# 1. Load the trained Potto model
model = joblib.load("ai/potto_model.pkl")
print("Potto AI model loaded successfully!")
# 2. Create a new road window
new_reading = {
    "mean_magnitude": 13.5,
    "max_magnitude": 17.2,
    "min_magnitude": 10.1,
    "std_magnitude": 1.8,
    "range_magnitude": 7.1
}
# 3. Convert the reading into a DataFrame
new_data = pd.DataFrame([new_reading])
# 4. Make a prediction
prediction = model.predict(new_data)
# 5. Get prediction probability
probabilities = model.predict_proba(new_data)
confidence = probabilities.max()
# 6. Display result
print("POTTO AI PREDICTION")
print("Predicted road condition:")
print(prediction[0])
print(f"Confidence: {confidence * 100:.2f}%")
