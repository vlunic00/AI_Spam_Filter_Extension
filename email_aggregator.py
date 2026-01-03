import pandas as pd
from pathlib import Path

##################################################
## @brief Iterate through files in a dir and aggregate them to a pandas dataframe 
## @in string           base_folder_path
## @out pd.DataFrame    df
##################################################
def aggregate_files_to_dataframe(base_folder_path):
    data = []
    
    base_path = Path(base_folder_path)
    
    for label_dir in base_path.iterdir():
        if label_dir.is_dir():
            label_name = label_dir.name
            print(f"Processing class: {label_name}")

            for file_path in label_dir.iterdir():
                if file_path.is_file():
                    try:
                        text = file_path.read_text(encoding='utf-8', errors='ignore')

                        data.append({
                            'text': text,
                            'label': label_name,
                            'filename': file_path.name  # Kept for debugging
                        })
                    except Exception as e:
                        print(f"Skipping {file_path}: {e}")

    df = pd.DataFrame(data)
    return df

input_folder = "./Processed Emails"

print("Aggregating files...")
df = aggregate_files_to_dataframe(input_folder)

output_file = "email_dataset_final.parquet" 
df.to_parquet(output_file, index=False)

print(f"Success! Saved {len(df)} rows to {output_file}")
print(df.head())