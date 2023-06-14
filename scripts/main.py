from pathlib import Path

from bereal_gpt.described_memory import DescribedMemory

directory = Path(__file__).parent.parent

memories = DescribedMemory.from_directory(directory / "memories")

for memory in memories:
    print(memory.primary_description())
