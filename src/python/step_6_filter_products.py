import pandas as pd
import re
import os
import argparse

def filter_products(df, args):
    """Filters the dataframe based on the provided requirements."""
    print('Filtering products based on your requirements...')
    
    # Filter by RAM
    if args.ram is not None:
        df['ram_numeric'] = df['ram_quantidade'].str.extract(r'(\d+)').astype(float)
        df = df[df['ram_numeric'] >= args.ram]
        df.drop(columns=['ram_numeric'], inplace=True)
        print(f"Filtered by RAM: >= {args.ram}GB")

    # Filter by Storage Type
    if args.storage_type is not None:
        df = df[df['armazenamento_tipo'].str.contains(args.storage_type, case=False, na=False)]
        print(f"Filtered by Storage Type: {args.storage_type}")

    # Filter by Processor
    if args.processor_keywords is not None:
        keyword_pattern = '|'.join(args.processor_keywords)
        df = df[df['processador'].str.contains(keyword_pattern, case=False, na=False)]
        print(f"Filtered by Processor Keywords: {', '.join(args.processor_keywords)}")

    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filter products based on requirements.')
    parser.add_argument('--ram', type=int, help='Minimum RAM in GB')
    parser.add_argument('--storage-type', type=str, help='Storage type (SSD or HDD)')
    parser.add_argument('--processor-keywords', nargs='+', help='Keywords to find in the processor description')
    
    args = parser.parse_args()

    # Define file paths
    script_dir = os.path.dirname(__file__)
    processed_file = os.path.join(script_dir, '../../data/processed_products.csv')
    finalists_file = os.path.join(script_dir, '../../data/finalists_products.csv')

    # Load the processed data
    if os.path.exists(processed_file):
        df = pd.read_csv(processed_file)
        
        # Apply the filters
        finalists_df = filter_products(df.copy(), args)
        
        print(f'\nFound {len(finalists_df)} products that meet your criteria.')
        
        # Save the finalists
        finalists_df.to_csv(finalists_file, index=False)
        print(f'Finalists saved to {finalists_file}')
    else:
        print(f'Error: Processed data file not found at {processed_file}')
