import re, json

def clean_affix_file_text(input_file: str, output_file: str):
    """Clean original affixes data, to work with them"""
    def clean_text(text: str) -> str:
        def replace_brackets(match):
            content = match.group(1)
            parts = content.split('|')
            return parts[-1]

        return re.sub(r'\[([^\]]+)\]', replace_brackets, text)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for category in data['result']:
        if 'entries' in category:
            for entry in category['entries']:
                if 'text' in entry:
                    entry['text'] = clean_text(entry['text'])
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f'Cleared file saved into: {output_file}')

input_path = 'files/affix_info2.txt'
output_path = 'files/cleared_affix.txt'

clean_affix_file_text(input_path, output_path)
