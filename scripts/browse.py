from pathlib import Path

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from bereal_gpt.alternate_reality import AlternateReality

directory = Path(__file__).parent.parent


def create_panel(alternate_reality: AlternateReality):
    alternate_reality_image = alternate_reality.image()
    memory = alternate_reality.described_memory.memory
    primary = memory.primary_image()
    secondary = memory.secondary_image()
    # Resize images to the same size if needed
    primary = primary.resize(alternate_reality_image.size)
    secondary = secondary.resize(alternate_reality_image.size)

    # Define the panel size (considering image sizes and text space)
    panel_size = (primary.width * 3, primary.height + 60)  # 60 pixels for text

    # Create a new image with white background
    panel = Image.new('RGB', panel_size, (255, 255, 255))

    # Paste the images into the panel
    panel.paste(primary, (0, 60))  # First image at (0,60)
    panel.paste(alternate_reality_image, (primary.width, 60))  # Second image beside the first one
    panel.paste(secondary, (primary.width * 2, 60))  # Third image beside the second one

    # Add text
    draw = ImageDraw.Draw(panel)
    draw.text((10, 10), alternate_reality.described_memory.primary_description(), fill="black")

    # Save the panel
    panel.save(directory / "browse" / f"{memory.memory_day()}.png")


alternate_realities = AlternateReality.from_directory(directory / "memories")
for alternate_reality in alternate_realities:
    print(alternate_reality.described_memory.memory.memory_day())
    try:
        create_panel(alternate_reality)
    except Exception as e:
        print(e)
