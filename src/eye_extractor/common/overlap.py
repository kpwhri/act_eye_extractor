class IndexOverlapChecker:

    def __init__(self):
        self.indices = []

    def add(self, start, end):
        """Where text could be identified as text[start:end], so end is exclusive"""
        self.indices.append((start, end))

    def overlaps(self, index):
        for start, end in self.indices:
            if start <= index < end:
                return True
        return False
