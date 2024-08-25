import os
import re
import pandas as pd
import ast
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sklearn
from sklearn.preprocessing import MinMaxScaler


class logs_analysis:
    def __init__(self, root_dir, create_or_not, do_we_delete):
        self.create_or_not = create_or_not
        self.root_dir = root_dir
        self.do_we_delete = do_we_delete
        self.files_paths = self.find_file_paths(root_dir=self.root_dir)
        self.df = self.create_dataframe()

    def find_file_paths(self, root_dir):
        def find_all_files(root_dir):
            file_list = []
            for dirpath, _, filenames in os.walk(root_dir):
                for filename in filenames:
                    file_list.append(os.path.join(dirpath, filename))
            return file_list

        all_files = find_all_files(root_dir)
        filtered_files = [
            file
            for file in all_files
            if not any(file.endswith(f"{i}.in") for i in range(1, 15))
        ]
        return filtered_files[1:]

    def delete_files(self):

        exclude_files = [f"{i}.in" for i in range(1, 15)]

        for dirpath, dirnames, filenames in os.walk(self.root_dir, topdown=False):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if filename not in exclude_files:
                    try:
                        os.remove(file_path)
                    except FileNotFoundError:
                        print(f"File not found: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")

            for dirname in dirnames:
                dir_to_remove = os.path.join(dirpath, dirname)
                try:
                    os.rmdir(dir_to_remove)
                    # print(f"Deleted directory: {dir_to_remove}")
                except OSError:
                    print(f"Directory not empty: {dir_to_remove}")

    def extract_log_data(self, file_path):
        with open(file_path, "r", encoding="ISO-8859-1") as file:
            content = file.read()

            # Use regex to find the required information
            best_node = re.search(r"Best Node:\s*(.+)", content)
            preprocess_time = re.search(
                r"Time to preprocess the data:\s*([\d.]+) seconds", content
            )
            solution_time = re.search(
                r"Time to find the solution:\s*([\d.]+) seconds", content
            )
            total_time = re.search(r"Total time:\s*([\d.]+) seconds", content)
            simulation_dict = re.search(r"Simulation dictionnary:\s*(.+)", content)
            nb_children = re.search(r"Number of childrens:\s*(.+)", content)
            expansion_policy = re.search(r"Desired expansion policy:\s*(.+)", content)
            desired_simulation_policy = re.search(
                r"Desired simulation policy:\s*(.+)", content
            )
            desired_selection_policy = re.search(
                r"Desired selection policy:\s*(.+)", content
            )
            cp = re.search(r"Cp:\s*(.+)", content)
            ratio = re.search(r"Ratio expansion:\s*(.+)", content)
            instance = re.search(r"Instance:\s*(.+)", content)

            # Count occurrences of SELECTION and SIMULATION
            num_selections = len(re.findall(r"SELECTION", content))
            num_simulations = len(re.findall(r"SIMULATION", content))

            # Extracted values (if found)
            best_node = best_node.group(1) if best_node else None
            preprocess_time = (
                preprocess_time.group(1) if preprocess_time else "Not found"
            )
            solution_time = solution_time.group(1) if solution_time else "Not found"
            total_time = total_time.group(1) if total_time else "Not found"
            simulation_dict = simulation_dict.group(1) if simulation_dict else None
            nb_children = nb_children.group(1) if nb_children else "Not found"
            expansion_policy = (
                expansion_policy.group(1) if expansion_policy else "Not found"
            )
            ratio = ratio.group(1) if ratio else "Not found"
            desired_simulation_policy = (
                desired_simulation_policy.group(1)
                if desired_simulation_policy
                else "Not found"
            )
            desired_selection_policy = (
                desired_selection_policy.group(1)
                if desired_selection_policy
                else "Not found"
            )
            cp = cp.group(1) if cp else "Not found"
            instance = instance.group(1) if instance else "Not found"

            if best_node is None:
                best_node = {}
                best_node["current_day"] = ""
                best_node["path"] = ""
                best_node["total_cost"] = ""
            else:
                best_node = ast.literal_eval(best_node)

            if simulation_dict is None:
                simulation_dict = ""
            else:
                simulation_dict = ast.literal_eval(simulation_dict)

            return {
                "Best node - day": best_node.get("current_day"),
                "Best node - path": best_node.get("path"),
                "Best node - cost": best_node.get("total_cost"),
                "Time to preprocess the data": preprocess_time,
                "Time to find the solution": solution_time,
                "Total time": total_time,
                "Number of SELECTION phases": num_selections,
                "Number of SIMULATION phases": num_simulations,
                "Simulation dictionnary": simulation_dict,
                "Number childrens": nb_children,
                "Desired expansion policy": expansion_policy,
                "Desired simulation policy": desired_simulation_policy,
                "Desired selection policy": desired_selection_policy,
                "Ratio expansion": ratio,
                "Cp": cp,
                "Instance": instance,
            }

    def create_dataframe(self):
        if not self.create_or_not:
            parent_dir = os.path.dirname(self.root_dir)
            file_path = os.path.join(parent_dir, "Simulation output.xlsx")
            return pd.read_excel(file_path)
        else:
            data = []
            for file_path in self.files_paths:
                log_data = self.extract_log_data(file_path)
                log_data["File Path"] = file_path
                log_data["Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data.append(log_data)

            df = pd.DataFrame(data)
            if self.do_we_delete:
                self.delete_files()

        df["Time to preprocess the data"] = pd.to_numeric(
            df["Time to preprocess the data"], errors="coerce"
        )
        df["Time to find the solution"] = pd.to_numeric(
            df["Time to find the solution"], errors="coerce"
        )
        df["Total time"] = pd.to_numeric(df["Total time"], errors="coerce")
        df["Number childrens"] = pd.to_numeric(df["Number childrens"], errors="coerce")
        df["Cp"] = pd.to_numeric(df["Cp"], errors="coerce")
        df["Instance"] = pd.to_numeric(df["Instance"], errors="coerce")
        df["Ratio expansion"] = pd.to_numeric(df["Ratio expansion"], errors="coerce")

        parent_dir = os.path.dirname(self.root_dir)
        file_path = os.path.join(parent_dir, "Simulation output.xlsx")

        try:
            if os.path.exists(file_path):
                # Attempt to read the Excel file
                current_df = pd.read_excel(file_path)
                # Concatenate the current DataFrame with the existing one
                final_df = pd.concat([current_df, df])
                return final_df
            else:
                print(f"File {file_path} does not exist.")
                return None
        except Exception as e:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            print(f"An error occurred: {e}. Saving DataFrame as a pickle file.")
            df.to_pickle(f"pickle_{timestamp}.pkl")
            return None

        final_df.to_excel(file_path, index=False)

        return df


# logs_analysis(
#    root_dir="/Users/adslv/Documents/LU/Term 3/Kiwi_TSP_Challenge/Code/Flight connections dataset",
#    create_or_not=True,
#    do_we_delete=True,
# )
