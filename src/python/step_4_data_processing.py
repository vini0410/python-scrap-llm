import pandas as pd
import re
import argparse
import os
import json

from data_processing.mercado_livre_processing import process_mercado_livre_data
from data_processing.kabum_processing import process_kabum_data

def clean_and_extract_features(input_file, output_file):
    """
    Loads the product data, cleans it, extracts features, and saves the processed data.
    """
    try:
        products_data = []
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    products_data.append(json.loads(line))
        df = pd.DataFrame(products_data)

        # Remove a coluna 'Peso' no início, se ela existir
        if 'Peso' in df.columns:
            df.drop(columns=['Peso'], inplace=True)
        
        # Apply site-specific cleaning for 'preco'
        def clean_price(row):
            if row['site'] == 'kabum':
                price_str = str(row['preco']).replace('R$', '').replace('\u00a0', '').replace('.', '').replace(',', '.')
                return pd.to_numeric(price_str, errors='coerce')
            else: # For mercado_livre and others
                return pd.to_numeric(row['preco'], errors='coerce')
        
        df['preco'] = df.apply(clean_price, axis=1)

        df.dropna(subset=['preco'], inplace=True)
        print('Data loaded and cleaned successfully.')

        # Process data based on site
        processed_dfs = []
        for site_name in df['site'].unique():
            site_df = df[df['site'] == site_name].copy()
            # if site_name == 'mercado_livre':
            #     processed_dfs.append(process_mercado_livre_data(site_df))
            if site_name == 'kabum':
                processed_dfs.append(process_kabum_data(site_df))
            else:
                print(f"Processing for site '{site_name}' is not implemented.")
        
        if processed_dfs:
            final_df = pd.concat(processed_dfs, ignore_index=True)
            print('\n--- Processed Data ---')
            print(final_df[['titulo_produto', 'preco', 'site', 'processador', 'ram_quantidade', 'armazenamento_quantidade']].head())
            print("Saving processed data to CSV...")
            final_df.to_csv(output_file, index=False, encoding='utf-8')
            print(f'Data successfully exported to {output_file}')
        else:
            print("No data processed.")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_file}")
        return
    except Exception as e:
        print(f"An error occurred during data loading or cleaning: {e}")
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    script_dir = os.path.dirname(__file__)
    input_file = os.path.join(script_dir, '../../data/products_details.json')
    output_file = os.path.join(script_dir, '../../data/raw_products.csv')

    clean_and_extract_features(input_file, output_file)
