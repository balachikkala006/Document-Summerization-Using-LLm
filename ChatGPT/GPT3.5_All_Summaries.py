import openai
import pandas as pd
import re
from tqdm import tqdm

# Set up your OpenAI API key
openai.api_key = "sk-"

# Load the DataFrame from the Excel sheet
df = pd.read_excel("All_Patent.xlsx")

# Create a new DataFrame to store the summaries
output_df = pd.DataFrame(columns=['Abstract', 'Claims', 'Abstract Summary', 'Claims Summary', 'New Summary', 'New Summary Summary'])

# Iterate over the rows in the DataFrame
for index, row in tqdm(df.iterrows(), total=len(df), desc="Generating Summaries"):
    # Get the abstract and claims
    abstract = row['Abstract']
    claims = row['Claims']

    # Clean the abstract and claims text
    abstract = re.sub(r'[^\x00-\x7F]+', '', str(abstract))
    claims = re.sub(r'[^\x00-\x7F]+', '', str(claims))

    # Make a request to the OpenAI API for generating the abstract summary
    abstract_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates abstract summaries."},
            {"role": "user", "content": abstract}
        ]
    )

    # Extract the generated abstract summary from the API response
    abstract_summary = abstract_response.choices[0].message.content

    # Make a request to the OpenAI API for generating the claims summary
    claims_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates claims summaries."},
            {"role": "user", "content": claims}
        ]
    )

    # Extract the generated claims summary from the API response
    claims_summary = claims_response.choices[0].message.content

    # Combine the abstract and claims summaries
    new_summary_input = abstract_summary + ' ' + claims_summary

    # Make a request to the OpenAI API for generating the new summary
    new_summary_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates new summaries."},
            {"role": "user", "content": new_summary_input}
        ]
    )

    # Extract the generated new summary from the API response
    new_summary = new_summary_response.choices[0].message.content

    # Make a request to the OpenAI API for generating the summary of the new summary
    new_summary_summary_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates summaries."},
            {"role": "user", "content": new_summary}
        ]
    )

    # Extract the generated summary of the new summary from the API response
    new_summary_summary = new_summary_summary_response.choices[0].message.content

    # Append the row to the output DataFrame
    output_df = output_df.append({'Abstract': abstract, 'Claims': claims, 'Abstract Summary': abstract_summary,
                                  'Claims Summary': claims_summary, 'New Summary': new_summary, 'New Summary Summary': new_summary_summary},ignore_index=True)

# Save the output DataFrame to a new Excel file
output_df.to_excel("GPT3.5_All_Summaries.xlsx", index=False)

