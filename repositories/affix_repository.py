import pandas as pd

class AffixRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.affixes = None

    def load_affixes(self):
        """Load affixes from a file"""
        if self.affixes is None:
            df = pd.read_json(self.file_path)
            self.affixes = pd.json_normalize(df['result'], 'entries')
        return self.affixes
    
    def find_affix_by_text(self, normalized_text: dict):
        """Find affix by text"""
        affixes = self.load_affixes()

        filtered = affixes[affixes['text'].str.contains(normalized_text['text'], regex=False, na=False)]

        if 'value' in normalized_text and normalized_text['value'] is not None:
            if 'value' in affixes.columns:
                filtered = filtered[filtered['value'] == normalized_text['value']]

        return filtered.iloc[0] if not filtered.empty else None
