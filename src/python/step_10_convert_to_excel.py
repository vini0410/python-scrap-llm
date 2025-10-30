import pandas as pd
import os
import argparse

def convert_csv_to_excel(input_file, output_file):
    """
    Reads a CSV file and converts it to an Excel file (.xlsx).
    """
    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"Error: Input file not found at {input_file}")
            return

        # Read the CSV data
        df = pd.read_csv(input_file)

        # Format the link column to be clickable in spreadsheets
        if 'link' in df.columns:
            # Sanitize URL by removing the fragment (#) and escaping XML special characters like '&'
            df['link'] = df['link'].apply(lambda url: f'=HYPERLINK("{str(url).split("#")[0].replace("&", "&amp;")}", "Ver Produto")')

        # Write to Excel
        # The 'openpyxl' engine is required for .xlsx files.
        # The HYPERLINK formulas should be interpreted correctly by Excel.
        df.to_excel(output_file, index=False, engine='openpyxl')

        print(f"Successfully converted {input_file} to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a CSV file to an Excel file.')
    
    # Default file paths relative to the script's location
    script_dir = os.path.dirname(__file__)
    default_input = os.path.join(script_dir, '../../data/processed_products.csv')
    default_output = os.path.join(script_dir, '../../data/processed_products.xlsx')

    parser.add_argument('--input', type=str, default=default_input, help='Path to the input CSV file.')
    parser.add_argument('--output', type=str, default=default_output, help='Path for the output Excel file.')
    
    args = parser.parse_args()

    convert_csv_to_excel(args.input, args.output)
