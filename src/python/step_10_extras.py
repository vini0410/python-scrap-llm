import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_data(input_file):
    """
    Visualizes the product data.
    """
    try:
        df = pd.read_csv(input_file)
        if not df.empty:
            df_sorted = df.sort_values('preco', ascending=False).reset_index(drop=True)
            print('Top products by price:')
            print(df_sorted[['titulo_produto', 'preco']])

            sns.set_style('whitegrid')
            plt.figure(figsize=(12, 8))

            sns.barplot(x='preco', y='titulo_produto', data=df_sorted)

            plt.title('Product Price Comparison', fontsize=16)
            plt.xlabel('Price (R$)', fontsize=12)
            plt.ylabel('Product', fontsize=12)
            plt.tight_layout()
            plt.show()

    except FileNotFoundError:
        print(f'{input_file} not found. Make sure the data processing step ran correctly.')

if __name__ == '__main__':
    visualize_data('../data/processed_products.csv')
