import os
import re

def replace_gls(match):
    word = match.group(1)
    before = match.group(0).split(word)[0]
    after = match.group(0).split(word)[1]

    # If the word is already wrapped with \gls{} or \Gls{}, return it as is.
    if (before.endswith('\\gls{') and after.startswith('}')) or (before.endswith('\\Gls{') and after.startswith('}')):
        return word

    # Check the case of the first character in the original word to determine the prefix
    prefix = '\\Gls{' if word[0].isupper() else '\\gls{'
    
    # Make the word lowercase and replace spaces with hyphens
    placeholder = word.lower().replace(' ', '-')
    return prefix + placeholder + '}'

acronyms = ['API', 'AWS', 'ECS', 'FIDO', 'IAM', 'IDP', 'JSON', 'JWT', 'NBIM', 'NTNU', 'OAuth 2.0', 'OIDC', 'OWASP', 'SAML', 'SP', 'SSO']
words_and_phrases = ['significant portion', 'digital identities', 'dog', 'road block']

script_directory = os.path.dirname(os.path.abspath(__file__))
input_file_path = os.path.join(script_directory, 'glossary.txt')
output_file_path = os.path.join(script_directory, 'output.txt')

with open(input_file_path, 'r', encoding='utf-8') as file:
    content = file.read()

    # Define patterns and replace words for acronyms
    acronym_pattern = r'(?<!\\\\gls{)(?<!\\\\Gls{)(\b(' + '|'.join(map(re.escape, acronyms)) + r')\b)(?!})'
    content = re.sub(acronym_pattern, replace_gls, content, flags=re.IGNORECASE)

    # Define patterns and replace words for words and phrases
    words_pattern = r'(?<!\\\\gls{)(?<!\\\\Gls{)(\b(' + '|'.join(map(re.escape, words_and_phrases)) + r')\b)(?!})'
    content = re.sub(words_pattern, replace_gls, content, flags=re.IGNORECASE)

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(content)

print(f"Processed input from {input_file_path} and saved the output to {output_file_path}")
