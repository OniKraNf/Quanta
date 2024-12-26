import re
from models.affix import Affix

class ItemService:
    def __init__(self, affix_repository):
        self.affix_repository = affix_repository
        self.item_data = {}

    def get_normalized_text(self, raw_text: str) -> dict:
        lines = raw_text.splitlines()
        first_separator = next((i for i, line in enumerate(lines) if line.strip() == '--------'), None)

        class_match = re.search(r'Item Class:\s([^\n]+)', raw_text)
        self.item_data['class'] = class_match.group(1).strip() if class_match else None

        rarity_match = re.search(r"Rarity:\s([^\n]+)", raw_text)
        self.item_data['rarity'] = rarity_match.group(1).strip() if rarity_match else None

        if self.item_data['rarity'] not in ['Unique', 'Rare', 'Unique (Foil)']:
            name_match = lines[2] if len(lines) >= 3 else None
        else:
            name_match = lines[3] if len(lines) >= 4 else None
        self.item_data['name'] = name_match.strip() if name_match else None

        stats = []
        if first_separator is not None:
            for line in lines[first_separator + 1:]:
                if line.strip() == "--------":
                    break
                stats.append(line.strip())
        self.item_data['stats'] = stats

        item_level_match = re.search(r'Item Level:\s([^\n]+)', raw_text)
        self.item_data['item_level'] = item_level_match.group(1).strip() if item_level_match else None

        blocks = re.findall(r"--------\n(.*?)(?=\n--------|\Z)", raw_text, re.DOTALL)

        blocks = [block for block in blocks if block.strip() != 'Corrupted']

        if blocks:
            last_block = blocks[-1]
            suffix_list = [line.strip() for line in last_block.splitlines() if line.strip()]
            self.item_data['suffixes'] = suffix_list
        else:
            self.item_data['suffixes'] = []

        #item = Item(self.item_data['class'], self.item_data['rarity'], self.item_data['name'])
            
        return self.item_data

    @staticmethod
    def normalize_affix_text(raw_affix: str) -> str:
        """Normalize affix text"""
        item_val = re.search('\d+', raw_affix)
        value = int(item_val.group())
        normalized_text = re.sub(r'[+-]?[\d#.]+', '#', raw_affix).strip()
        return {'text': normalized_text, 'value': value}
    
    def get_normalized_affixes(self, raw_affixes: list):
        """Find normalized affixes for item"""
        normalized_affixes = []
        for raw_affix in raw_affixes.get('suffixes', []):
            normalized_text = self.normalize_affix_text(raw_affix)
            affix_data = self.affix_repository.find_affix_by_text(normalized_text)
            affix_data['value'] = normalized_text['value']
            if not affix_data.empty:
                affix = Affix(affix_data['id'], affix_data['text'], affix_data['type'], affix_data.get('value'))
                normalized_affixes.append(affix)
            else:
                print(f"Unknow affix: {raw_affix}")
        return normalized_affixes