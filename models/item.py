class Item:
    def __init__(self, item_class, rarity, name, stats, item_level, requirements):
        self.item_class = item_class
        self.rarity = rarity
        self.name = name
        self.stats = stats
        self.item_level = item_level
        self.affixes = []

    def add_affix(self, affix):
        self.affixes.append(affix)
    
