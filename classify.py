from transformers import ViTForImageClassification, ViTImageProcessor
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')
model.to(device)

processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')


def classify(image):
    inputs = processor(images=image, return_tensors="pt").to(device)
    pixel_values = inputs.pixel_values
    with torch.no_grad():
        outputs = model(pixel_values)
    logits = outputs.logits
    prediction = logits.argmax(-1)
    return model.config.id2label[prediction.item()]


if __name__ == "__main__":
    from pathlib import Path
    from PIL import Image

    image = Path(__file__).parent / "memories" / "2022-06-03" / "primary.jpg"
    image = Image.open(image)
    print(classify(image))
