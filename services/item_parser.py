import re

def parse_item_data(item_text: str) -> dict:
    item_data = {}

    class_match = re.search(r'Item Class:\s([^\n]+)', item_text)
    item_data['class'] = class_match.group(1).strip() if class_match else None

    rarity_match = re.search(r"Rarity:\s([^\n]+)", item_text)
    item_data['rarity'] = rarity_match.group(1).strip() if rarity_match else None

    blocks = re.findall(r"--------\n(.*?)(?=\n--------|\Z)", item_text, re.DOTALL)

    blocks = [block for block in blocks if block.strip() != 'Corrupted']

    if blocks:
        last_block = blocks[-1]
        suffix_list = [line.strip() for line in last_block.splitlines() if line.strip()]
        item_data['suffixes'] = suffix_list
    else:
        item_data['suffixes'] = []
        
    return item_data