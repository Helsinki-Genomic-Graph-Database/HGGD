class StubIO:
    def __init__(self, inputs = []):
        self.inputs = inputs
        self.inputs.append("short")
        self.inputs.append("short")
        self.outputs = []

    def read(self, text):
        return self.inputs.pop(0)

    def write(self, text):
        self.outputs.append(text)
