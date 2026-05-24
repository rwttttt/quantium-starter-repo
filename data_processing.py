import os
import pandas as pd

# Define paths
DATA_DIR = "./data"
OUTPUT_FILE = "formatted_data.csv"

# 1. EXTRACT: Find and collect all the CSV data files in the data folder
csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
combined_dfs = []

print(f"Found {len(csv_files)} raw data files to process...")

for file in csv_files:
    file_path = os.path.join(DATA_DIR, file)
    df = pd.read_csv(file_path)
    
    # 2. TRANSFORM: Clean and filter the data according to requirements
    
    # Requirement A: Filter rows where the product is exactly 'pink morsel' (case-insensitive)
    df['product'] = df['product'].str.strip().str.lower()
    df = df[df['product'] == 'pink morsel']
    
    if df.empty:
        continue
        
    # FORCE STRIP '$' from the price column and safely convert to numeric/float
    df['price'] = df['price'].astype(str).str.replace('$', '', regex=False).astype(float)
        
    # Requirement B: Combine quantity and price into a single 'sales' field (quantity * price)
    df['sales'] = df['quantity'] * df['price']
    
    # Requirement C: Keep only the three fields: sales, date, region
    df = df[['sales', 'date', 'region']]
    
    # Add this file's processed data to our list
    combined_dfs.append(df)

# 3. LOAD: Merge everything together and export to a single file
if combined_dfs:
    final_df = pd.concat(combined_dfs, ignore_index=True)
    
    # Format column names nicely to match standard conventions (Sales, Date, Region)
    final_df.columns = ['Sales', 'Date', 'Region']
    
    # Sort chronologically by Date so the visualization renders cleanly later
    final_df['Date'] = pd.to_datetime(final_df['Date'])
    final_df = final_df.sort_values(by='Date')
    
    # Save directly to the root of your repository
    final_df.to_csv(OUTPUT_FILE, index=False)
    print("🎉 Success! Beautifully formatted data saved to formatted_data.csv")
else:
    print("❌ Error: No Pink Morsel data found in the files.")