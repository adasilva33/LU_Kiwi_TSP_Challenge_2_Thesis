import os
import shutil


root_dir = "/Users/adslv/Documents/LU/Term 3/Kiwi_TSP_Challenge/Code/Flight connections dataset"

items = os.listdir(root_dir)
for item in items:
    item_path = os.path.join(root_dir, item)
    if os.path.isdir(item_path) and item.startswith(
        (
            "1.in_",
            "2.in_",
            "3.in_",
            "4.in_",
            "5.in_",
            "6.in_",
            "7.in_",
            "8.in_",
            "9.in_",
            "10.in_",
            "11.in_",
            "12.in_",
            "13.in_",
            "14.in_",
        )
    ):
        prefix = item.split("_")[0]
        destination_folder = os.path.join(root_dir, f"{prefix}_simulations")

        # Check if the destination folder exists or not
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        destination_path = os.path.join(destination_folder, item)

        # Make sure we aren't moving the folder into itself
        if item_path != destination_path:
            shutil.move(item_path, destination_path)
        else:
            print(
                f"Skipping move for '{item}' because it would result in moving the directory into itself."
            )

print("Folders have been successfully organized!")
