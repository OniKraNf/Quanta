class Affix:
    def __init__(self, id_, text, type_, value):
        self.id = id_
        self.text = text
        self.type = type_
        self.value = value

    def __str__(self):
        return f"{self.id, self.type, self.text, self.value}"

