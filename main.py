from pathlib import Path

from bereal_gpt.memories import Memory
from bereal_gpt.described_memory import DescribedMemory

directory = Path(__file__).parent
described_directory = directory / "described"

memories = Memory.from_directory(directory / "memories")

for memory in memories:
    print(memory.memory_day())
    described = DescribedMemory(memory)

    memory.primary_image().save(described_directory / f"{described.primary_description()}.jpg")
    memory.secondary_image().save(described_directory / f"{described.secondary_description()}.jpg")
