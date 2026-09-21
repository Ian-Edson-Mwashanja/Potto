import pandas as pd
# 1. Load the realistic road dataset
df = pd.read_csv("data/realistic_road_data.csv")
print("Original dataset:")
print(df.head())
print("\nTotal records:", len(df))
# 2. Define the size of our window
WINDOW_SIZE = 20
# 3. Create an empty list for features
feature_rows = []
# 4. Process the data in windows
for start in range(0, len(df), WINDOW_SIZE):
    window = df.iloc[start:start + WINDOW_SIZE]
    # Ignore incomplete windows
    if len(window) < WINDOW_SIZE:
        continue
    # Calculate features from magnitude
    mean_magnitude = window["magnitude"].mean()
    max_magnitude = window["magnitude"].max()
    min_magnitude = window["magnitude"].min()
    std_magnitude = window["magnitude"].std()
    range_magnitude = max_magnitude - min_magnitude
    # Get the most common label in the window
    label = window["label"].mode()[0]
    # Store the features
    feature_rows.append({
        "mean_magnitude": mean_magnitude,
        "max_magnitude": max_magnitude,
        "min_magnitude": min_magnitude,
        "std_magnitude": std_magnitude,
        "range_magnitude": range_magnitude,
        "label": label
    })
# 5. Convert features into a DataFrame
features_df = pd.DataFrame(feature_rows)
# 6. Display the result
print("\nFeature-engineered dataset:")
print(features_df.head())
print("\nNumber of windows:", len(features_df))
# 7. Display average features by class
print("\nAverage features by road type:")
print(
    features_df
    .groupby("label")
    .mean(numeric_only=True)
)
# 8. Save the new dataset
features_df.to_csv(
    "data/engineered_features.csv",
    index=False
)
print("\nFeature engineering completed!")
print("Saved to:")
print("data/engineered_features.csv")