from pathlib import Path

from bereal_gpt.alternate_reality import AlternateReality

directory = Path(__file__).parent.parent

for style in ('anime', 'impressionism', 'claymation', 'pop art', 'watercolor', 'oil painting', 'sketch', 'cartoon'):
    for date in ("2023-04-17", "2023-05-22", "2023-06-04"):
        alternate_reality = AlternateReality.from_directory(directory / 'memories', style=style)
        alternate_reality[date].image().show()
