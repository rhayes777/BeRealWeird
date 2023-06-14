from pathlib import Path

from bereal_gpt.alternate_reality import AlternateReality

directory = Path(__file__).parent.parent
alternate_realities = AlternateReality.from_directory(directory / "memories")

for alternate_reality in alternate_realities:
    print(
        f"{alternate_reality.described_memory.memory.memory_day()}: {alternate_reality.described_memory.primary_description()}")
    alternate_reality.primary_image().show()
    alternate_reality.secondary_image().show()
