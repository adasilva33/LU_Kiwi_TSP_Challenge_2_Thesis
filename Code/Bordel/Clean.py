import os
import pickle
import pandas as pd

root_dir = "/Users/adslv/Documents/LU/Term 3/Kiwi_TSP_Challenge/Code/Pickle Instance 1"

# List to hold data from all pickles
dataframes = []

# Loop over all files in the directory
for filename in os.listdir(root_dir):
    if filename.endswith(".pkl"):
        filepath = os.path.join(root_dir, filename)
        print(f"Loading {filename}")

        # Load the pickle file
        with open(filepath, "rb") as file:
            data = pickle.load(file)

            # Assuming each pickle file contains a DataFrame
            dataframes.append(data)

# Concatenate all DataFrames
if dataframes:
    final_df = pd.concat(dataframes, ignore_index=True)

    # Save the final concatenated DataFrame as a pickle file
    final_df_path = os.path.join(root_dir, "final_df.pkl")
    with open(final_df_path, "wb") as final_file:
        pickle.dump(final_df, final_file)

    print(f"Final DataFrame saved to {final_df_path}")
