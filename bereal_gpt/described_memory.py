from .memories import Memory
from .describe import describe


class DescribedMemory:
    def __init__(self, memory: Memory):
        self.memory = memory

        if not self.primary_description_path.exists():
            self.primary_description_path.write_text(
                describe([memory.primary_image()])[0]
            )
        if not self.secondary_description_path.exists():
            self.secondary_description_path.write_text(
                describe([memory.secondary_image()])[0]
            )

    @property
    def primary_description_path(self):
        return self.memory.path / "primary_description.txt"

    @property
    def secondary_description_path(self):
        return self.memory.path / "secondary_description.txt"

    def primary_description(self):
        return self.primary_description_path.read_text()

    def secondary_description(self):
        return self.secondary_description_path.read_text()
