import pandas as pd
import re


def load_affix_data(file_path: str): 
    """Load and normalize affix data from file"""
    df = pd.read_json('affix_info.txt')
    return pd.json_normalize(df['result'], 'entries')


def clean_suffix_text(suffix: str) -> str:
    """Normalize suffix text for comprasion."""
    suffix = re.sub(r'[+-]?[\d#.]+', '#', suffix)
    return suffix.strip()
    

def find_suffix(item_data: dict):
    """Find and normalize suffix using the affix_data"""


def clean_suffix_text(suffix: str) -> str:
    suffix = re.sub(r'[+-]?[\d#.]+', '#', suffix)
    if suffix.find('Resistance'):
        suffix = re.sub(r'')
    print(f'after: {suffix}')
    return suffix


test_data = {
    'class': 'Bows',
    'rarity': 'Rare',
    'suffixes': [
        '+15% to Cold Resistance',
        'Adds 4 to 56 Lightning Damage',
        '+87 to Accuracy Rating',
        '+2 to Level of all Projectile Skills',
        '+27 to Dexterity',
        'Gain 5 Life per Enemy Killed'
    ]
}


find_suffix(test_data)
