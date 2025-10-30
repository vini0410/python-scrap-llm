import pandas as pd
import re

def _create_searchable_string(row):
    """Creates a single string from multiple columns for easier searching."""
    search_string = ""
    if 'titulo_produto' in row and row['titulo_produto']:
        search_string += str(row['titulo_produto']) + ' '
    if 'descricao' in row and row['descricao']:
        search_string += str(row['descricao']) + ' '
    return search_string

def _extract_screen_size(text):
    match = re.search(r'(\d+\.?\d*)\s*(?:polegadas|pol|\'|"|")', text, re.IGNORECASE)
    if match:
        return match.group(1) + ' polegadas'
    return None

def _extract_processor(text):
    # Regex to find common processor models
    pattern = r'(intel\s+(?:core\s+(?:ultra\s+[\w-]+|i\d(?:-[\w\d]+)?)|celeron(?:[\s-][\w\d]+)?|pentium(?:[\s-][\w\d]+)?)|amd\s+ryzen\s+\d+(?:[\s-][\w\d]+)?|apple\s+m\d+(?:\s+pro|\s+max)?)'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(0)
    return None

def _extract_ram_info(text):
    ram_quantity = None
    ram_type_speed = None
    
    # Regex for RAM quantity (e.g., 8GB, 16G, 32 GB)
    quantity_match = re.search(r'(\d+)\s*(gb|g)\s*(?:de\s+)?ram', text, re.IGNORECASE)
    if not quantity_match:
        quantity_match = re.search(r'ram\s+(\d+)\s*(gb|g)', text, re.IGNORECASE)
    if quantity_match:
        ram_quantity = quantity_match.group(1) + 'GB'

    # Regex for RAM type/speed (e.g., DDR4, LPDDR5, 3200MHz)
    type_speed_match = re.search(r'(ddr\d+|lpddr\d*x?|sodimm|\d+mhz)', text, re.IGNORECASE)
    if type_speed_match:
        ram_type_speed = type_speed_match.group(0).upper()
        
    return ram_quantity, ram_type_speed

def _extract_storage_info(text):
    storage_quantity = None
    storage_type = None
    
    # Regex for storage (e.g., 512GB SSD, 1TB HDD, 256 GB NVMe)
    match = re.search(r'(\d+)\s*(gb|tb)\s*(ssd|hdd|nvme|emmc)', text, re.IGNORECASE)
    if match:
        storage_quantity = match.group(1) + match.group(2).upper()
        storage_type = match.group(3).upper()
        if storage_type == 'NVME':
            storage_type = 'NVME SSD'
    
    return storage_quantity, storage_type

def process_kabum_data(df):
    print("Processing Kabum data with unified extraction...")

    # Create the searchable string column
    df['informacoes_produto'] = df.apply(_create_searchable_string, axis=1)
    
    # --- Feature Extraction ---
    df['tamanho_tela'] = df['informacoes_produto'].apply(_extract_screen_size)
    print('Screen size extracted for Kabum.')

    df['processador'] = df['informacoes_produto'].apply(_extract_processor)
    print('Processor information extracted for Kabum.')

    df[['ram_quantidade', 'ram_tipo_velocidade']] = df['informacoes_produto'].apply(
        lambda x: pd.Series(_extract_ram_info(x))
    )
    print('RAM information extracted for Kabum.')

    df[['armazenamento_quantidade', 'armazenamento_tipo']] = df['informacoes_produto'].apply(
        lambda x: pd.Series(_extract_storage_info(x))
    )
    print('Storage information extracted for Kabum.')

    # Drop the temporary column
    df.drop(columns=['informacoes_produto'], inplace=True)
    
    return df