from pathlib import Path

from .memories import Memory


def _add_description(image_function, description_path: Path, ):
    if not description_path:
        from .describe import describe
        description_path.write_text(
            describe([image_function()])[0]
        )


class DescribedMemory:
    def __init__(self, memory: Memory):
        self.memory = memory

        _add_description(
            memory.primary_image,
            self.primary_description_path,
        )
        _add_description(
            memory.secondary_image,
            self.secondary_description_path,
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

    @classmethod
    def from_directory(cls, directory):
        return list(map(cls, Memory.from_directory(directory)))
