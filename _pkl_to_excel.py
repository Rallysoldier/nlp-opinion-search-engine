import pickle
import pandas as pd
import os
import sys

def pkl_to_excel(input_pkl, output_folder):
    """
    Convert any .pkl file to an Excel file and save it to a specified folder.
    
    Args:
        input_pkl (str): Path to the .pkl file.
        output_folder (str): Path to the folder where the Excel file should be saved.
    """
    # Ensure the input file exists
    if not os.path.isfile(input_pkl):
        print(f"Error: File '{input_pkl}' does not exist.")
        sys.exit(1)

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Generate output file name
    base_name = os.path.splitext(os.path.basename(input_pkl))[0]
    output_excel = os.path.join(output_folder, f"{base_name}.xlsx")

    # Load the .pkl file
    try:
        with open(input_pkl, "rb") as f:
            data = pickle.load(f)
    except Exception as e:
        print(f"Error loading .pkl file: {e}")
        sys.exit(1)

    # Convert the data to a DataFrame for saving to Excel
    try:
        if isinstance(data, pd.DataFrame):
            df = data
        elif isinstance(data, dict):
            # Convert dictionary to DataFrame
            df = pd.DataFrame(list(data.items()), columns=["Key", "Value"])
        elif isinstance(data, list):
            # Convert list to DataFrame
            df = pd.DataFrame(data)
        else:
            print("Error: Unsupported data type in .pkl file. Must be a DataFrame, dict, or list.")
            sys.exit(1)
        
        # Save the DataFrame to Excel
        df.to_excel(output_excel, index=False)
        print(f"Data successfully saved to '{output_excel}'")

    except Exception as e:
        print(f"Error converting .pkl to Excel: {e}")
        sys.exit(1)

# Main block to run the function from the command line
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pkl_to_excel.py <input_pkl>")
        sys.exit(1)

    input_pkl = sys.argv[1]
    output_folder = r"C:\Users\Rallysoldier\Documents\4397_COSC\res_proj_helper_files"

    pkl_to_excel(input_pkl, output_folder)
