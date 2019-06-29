class VariableUse:
    def __init__(self, name, is_array=0, start_index=0, end_index=0):
        self.name = name
        self.assignments = 0
        self.uses = 0
        self.max_nesting = 0
        self.is_array = is_array
        self.start_index = start_index
        self.end_index = end_index
        self.length = end_index - start_index