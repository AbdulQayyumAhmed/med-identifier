import pandas as pd
import os

def clean_data(input_path, output_path):
    df = pd.read_csv(input_path)
    
    df = df.fillna('Information not available')
    
    initial_count = len(df)
    df = df.drop_duplicates(subset=['brand_name', 'generic_name'])
    final_count = len(df)
    if initial_count != final_count:
        print(f"Removed {initial_count - final_count} redundant records.")
    
    df['combined_text'] = (
        "Brand: " + df['brand_name'] + " | " +
        "Generic: " + df['generic_name'] + " | " +
        "Dosages: " + df['dosage'] + " | " +
        "Form: " + df['dosage_form'] + " | " +
        "Uses: " + df['indications'] + " | " +
        "Side Effects: " + df['side_effects'] + " | " +
        "Source: " + df['source']
    )
    
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")
    return df

if __name__ == "__main__":
    input_file = os.path.join('data', 'medicine_data.csv')
    output_file = os.path.join('data', 'medicine_cleaned.csv')
    
    if os.path.exists(input_file):
        clean_data(input_file, output_file)
    else:
        print(f"Error: {input_file} not found.")
