#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 15:46:20 2024

@author: swetha
"""

import os
import pandas as pd

# Folder containing the Excel files
folder_path = "/Users/swetha/Documents/Work/All_diploma_collegedetails"
output_file = "/Users/swetha/Documents/Work/merged_data/merged_all_MD_allstates.xlsx"

# List to hold individual DataFrames
all_data_frames = []

# Loop through each file in the folder
for file_name in os.listdir(folder_path):
    # Check if the file is an Excel file
    if file_name.endswith(".xlsx"):
        file_path = os.path.join(folder_path, file_name)
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path)
        # Append the DataFrame to the list
        all_data_frames.append(df)

# Concatenate all DataFrames in the list
merged_data = pd.concat(all_data_frames, ignore_index=True)

# Write the merged DataFrame to a new Excel file
merged_data.to_excel(output_file, index=False)

print(f"All Excel files have been merged and saved to {output_file}")
