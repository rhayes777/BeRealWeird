import random
from pathlib import Path

from bereal_gpt.alternate_reality import AlternateReality

directory = Path(__file__).parent.parent

styles = ('anime', 'impressionism', 'claymation', 'pop art', 'watercolor', 'oil painting', 'sketch', 'cartoon')
style = random.choice(styles)
print(style)
alternate_reality = AlternateReality.from_directory(directory / 'memories', style=style)
reality = random.choice(list(alternate_reality))
print(
    f"Creating {reality.described_memory.description} from {reality.described_memory.memory.memory_day()} in style {style}")
comparison = reality.comparison_image()

comparison.show()
