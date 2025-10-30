import pandas as pd
import os
import argparse

def get_ai_recommendation_prompt(finalists_file, requirements):
    """Generates the prompt for the AI recommendation."""
    
    if os.path.exists(finalists_file):
        finalists_df = pd.read_csv(finalists_file)
        
        # Prepare the data for the prompt
        finalists_df_sorted = finalists_df
        products_data_for_prompt = finalists_df_sorted[['titulo_produto', 'preco', 'processador', 'ram_quantidade', 'armazenamento_quantidade', 'armazenamento_tipo', 'link']].to_markdown(index=False)
        
        # Create the prompt
        prompt = f"""
You are a helpful AI assistant and an expert in hardware analysis.
Your task is to analyze a list of notebooks that meet the user's minimum requirements and recommend the best options based on cost-benefit.

User's detailed preferences:
- Cost-benefit notebook, but with longevity in mind.
- Processor: Updated (preferably the latest version).
- RAM: At least 32 GB (preferably with good speed).
- Graphics Card: Dedicated graphics card is not necessary.

Here is the list of candidate notebooks:
{products_data_for_prompt}

Please perform the following analysis:
1.  **Ranked Cost-Benefit List (up to 10 notebooks):** Provide a ranked list of up to 10 notebooks from the provided list, ordered by their cost-benefit. The first item should be the absolute best cost-benefit option.
2.  **Detailed Explanation for Each:** For each notebook in the ranked list, provide a concise explanation. For items ranked lower than the first, explain why they are less ideal in terms of cost-benefit. This could include:
    *   If it's more expensive: Explain if the increased cost brings significant, minor, or negligible additional value (e.g., 'more expensive but offers only a marginal performance increase not justifying the price').
    *   If it's cheaper: Explain what important features or performance aspects might be missing or compromised (e.g., 'cheaper but lacks the latest generation processor, which might impact long-term usability').
3.  **Final Summary:** Provide a concise, overall recommendation to the user, summarizing the key takeaways from the ranked list.

Present your analysis in a clear, easy-to-read format.
"""
        
        print("--- Prompt for AI Analysis ---")
        print(prompt)
        print("\n--- End of Prompt ---")
        
        # In a real scenario, you would send this prompt to a large language model.
        # For this demonstration, the AI (Gemini) will provide the analysis in the next step.
        print("\nNow, I will analyze the products based on the prompt above and provide the recommendation.")
    else:
        print(f'Error: Finalists file not found at {finalists_file}. Please run Step 8 first.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate AI recommendation prompt.')
    parser.add_argument('--ram', type=int, help='Minimum RAM in GB')
    parser.add_argument('--storage-type', type=str, help='Storage type (SSD or HDD)')
    parser.add_argument('--processor-keywords', nargs='+', help='Keywords to find in the processor description')
    
    args = parser.parse_args()
    
    # Define file paths
    script_dir = os.path.dirname(__file__)
    finalists_file = os.path.join(script_dir, '../../data/finalists_products.csv')
    
    # Create a dictionary from the arguments to pass to the prompt function
    requirements = {
        'ram_quantidade': args.ram,
        'armazenamento_tipo': args.storage_type,
        'processador_keywords': args.processor_keywords
    }
    
    get_ai_recommendation_prompt(finalists_file, requirements)
