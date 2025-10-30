import json
import os

def convert_jsonlines_to_json(input_file, output_file):
    """
    Converts a JSON Lines file to a standard JSON array file.
    """
    print(f"Converting {input_file} to {output_file}...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = [json.loads(line) for line in f if line.strip()]

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Successfully converted {len(data)} items.")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    input_f = os.path.join(script_dir, '../../data/products_details.json')
    output_f = os.path.join(script_dir, '../../data/products_details_formatted.json')
    convert_jsonlines_to_json(input_f, output_f)
