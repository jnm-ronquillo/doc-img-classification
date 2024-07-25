import os
import pandas as pd
import matplotlib.pyplot as plt


def create_dataframe_from_folders(base_path):
    data = []

    # Iterate through each folder in the base path
    for category in os.listdir(base_path):
        category_path = os.path.join(base_path, category)

        # Check if it's a directory
        if os.path.isdir(category_path):
            # Iterate through files in the category folder
            for filename in os.listdir(category_path):
                file_path = os.path.join(category_path, filename)

                # You may want to add more conditions here to filter specific file types
                if os.path.isfile(file_path):
                    # Add a row to our data list
                    data.append({
                        'category': category,
                        'filename': filename,
                        'filepath': file_path
                        # Add more columns as needed
                    })

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)
    return df


def plot_group_histogram(df, group_col):
    # Group the DataFrame by the specified column and count the number of rows per group
    group_counts = df.groupby(group_col).size()

    # Create a histogram plot
    plt.figure(figsize=(10, 6))
    plt.bar(group_counts.index, group_counts.values)

    # Set the plot title and labels
    plt.title(f"Number of Rows per {group_col}")
    plt.xlabel(group_col)
    plt.ylabel("Number of Rows")

    # Rotate the x-axis labels if needed
    plt.xticks(rotation=45, ha='right')

    # Adjust the plot layout
    plt.tight_layout()


def oversample_dataframe(df, target_multiply=1):
    df_grouped = df.groupby('category')

    # Find the size of the biggest category group
    target_size = df_grouped.size().max() * target_multiply

    df_oversampled = pd.DataFrame()
    for category, group_data in df_grouped:
        num_rows = len(group_data)

        if num_rows < target_size:
            num_duplicates = target_size - num_rows
            duplicates = group_data.sample(n=num_duplicates, replace=True)

            # Reset the index to create a continuous index for each category
            group_data = group_data.reset_index(drop=True)
            duplicates = duplicates.reset_index(drop=True)

            # Create a new column 'duplication_number' with the duplication number
            group_data['duplication_number'] = 0
            duplicates['duplication_number'] = duplicates.groupby('filename').cumcount() + 1

            df_oversampled = pd.concat([df_oversampled, group_data, duplicates])
        else:
            group_data['duplication_number'] = 0
            df_oversampled = pd.concat([df_oversampled, group_data])

    # Reset the index of the oversampled DataFrame
    df_oversampled = df_oversampled.reset_index(drop=True)

    return df_oversampled
