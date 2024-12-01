import pickle
import pandas as pd

'''REMEMBER: Your method files are returning the ID - 2. It is very likely that the reviews segment is being
improperly converted into a dataframe somehwere. DO NOT FORGET'''

# Load the reviews segment and create a DataFrame
with open("reviews_segment.pkl", "rb") as f:
    reviews_segment = pickle.load(f)

segment_df = pd.DataFrame(reviews_segment)
segment_df["ID"] = segment_df.index + 2  # Add ID column based on the index
segment_df_result = segment_df[["ID", "review_text"]]  # Filter relevant columns
print(segment_df_result.head())

''' CHOOSE INPUT FILE: '''
result_files = {
    "1": "audio_quality_poor_method1.pkl",
    "2": "audio_quality_poor_method2.pkl",
    "3": "audio_quality_poor_method3.pkl",

    "4": "wifi_signal_strong_method1.pkl",
    "5": "wifi_signal_strong_method2.pkl",
    "6": "wifi_signal_strong_method3.pkl",

    "7": "gps_map_useful_method1.pkl",
    "8": "gps_map_useful_method2.pkl",
    "9": "gps_map_useful_method3.pkl",

    "10": "image_quality_sharp_method1.pkl",
    "11": "image_quality_sharp_method2.pkl",
    "12": "image_quality_sharp_method3.pkl",
}
valid_input:bool = None
while(valid_input == None):
    user_input = input("Choose a result to analyze (1-12): ")
    if user_input in result_files:
        valid_input = True
        input_pkl = result_files[user_input]
    else:
        print("Invalid Input\n")
        continue

with open(input_pkl, "rb") as f:
    result_ids = pickle.load(f)

result_df = pd.DataFrame(result_ids)
# Add 2 to the only column, no matter its name
result_df[result_df.columns[0]] = result_df[result_df.columns[0]] + 2
print(result_df.head())

# Prepare an empty DataFrame for the output
output_df = pd.DataFrame(columns=["ID", "review_text"])
print(output_df.head())

# Collect IDs from result_df
IDs = result_df["review_index"].tolist()
print(f"# of IDs from boolean search: {len(IDs)}")

# Add rows to the output DataFrame
for i, ID in enumerate(IDs):
    # Find the matching review text for the given ID
    matching_review = segment_df.loc[segment_df["ID"] == ID, "review_text"]
    
    if not matching_review.empty:  # Check if a match is found
        output_df.loc[i, "ID"] = ID
        output_df.loc[i, "review_text"] = matching_review.iloc[0]  # Get the first matching text

print(output_df.head())
output_folder = r"C:\Users\Rallysoldier\Documents\4397_COSC\res_proj_helper_files"
custom_name = input_pkl + "_rev_text"
output_path = rf"{output_folder}\{custom_name}.xlsx"

# Save the DataFrame to an Excel file
output_df.to_excel(output_path, index=False)  # index=False prevents adding a new index column

print(f"DataFrame successfully saved to {output_path}")
