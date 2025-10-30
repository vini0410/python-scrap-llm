import pandas as pd
import os

def export_to_csv(input_file, output_file):
    """
    Exports the processed data to a CSV file.
    """
    try:
        df = pd.read_csv(input_file)
        columns_to_export = [
            'titulo_produto',
            'processador',
            'ram_quantidade',
            'ram_tipo_velocidade',
            'armazenamento_quantidade',
            'armazenamento_tipo',
            'preco',
            'tamanho_tela',
            'link'
        ]
        existing_columns = [col for col in columns_to_export if col in df.columns]

        if existing_columns:
            df[existing_columns].to_csv(output_file, index=False, encoding='utf-8')
            print(f'Data successfully exported to {output_file}')
        else:
            print('No relevant columns found to export.')

    except FileNotFoundError:
        print(f'{input_file} not found. Make sure the data processing step ran correctly.')

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    input_file = os.path.join(script_dir, '../../data/raw_products.csv')
    output_file = os.path.join(script_dir, '../../data/processed_products.csv')
    export_to_csv(input_file, output_file)
