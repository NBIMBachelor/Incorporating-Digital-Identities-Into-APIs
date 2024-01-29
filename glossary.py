import os
import re

# List of words to search for
words_to_highlight = ['API', 'AWS', 'ECS', 'FIDO', 'IAM', 'IDP', 'JSON', 'JWT', 'NBIM', 'NTNU', 'OAuth 2.0', 'OIDC', 'OWASP', 'SAML', 'SP', 'SSO']

# Get the directory where the Python script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Input file path in the same directory as the script
input_file_path = os.path.join(script_directory, 'glossary.txt')

# Output file path in the same directory as the script
output_file_path = os.path.join(script_directory, 'output.txt')

# Open the input file for reading
with open(input_file_path, 'r', encoding='utf-8') as file:
    # Read the content of the file
    content = file.read()

    # Define a regular expression pattern to match the exact words
    pattern = r'\b(' + '|'.join(map(re.escape, words_to_highlight)) + r')\b'

    # Replace the matched words with \gls{word}n
    highlighted_content = re.sub(pattern, r'\\gls{\1}', content)

# Open the output file for writing
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Write the modified content to the output file
    output_file.write(highlighted_content)

print(f"Processed input from {input_file_path} and saved the output to {output_file_path}")
