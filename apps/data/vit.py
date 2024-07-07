import os
import cv2
import torch
import numpy as np
import pyheif
from PIL import Image
from rembg import remove
from torchvision import transforms
import timm
import torch.nn.functional as F

class RheumatoidArthritisDetector:
    def __init__(self, model_checkpoint, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.load_model(model_checkpoint)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])

    def load_model(self, model_checkpoint):
        model = timm.create_model('vit_base_patch16_224.augreg_in21k', pretrained=False, num_classes=2)
        checkpoint = torch.load(model_checkpoint, map_location=self.device)
        model.load_state_dict(checkpoint)
        model.to(self.device)
        model.eval()
        return model

    def convert_heic_to_image(self, heic_path):
        heif_file = pyheif.read(heic_path)
        return Image.frombytes(
            heif_file.mode, 
            heif_file.size, 
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )

    def convert_to_jpg(self, input_directory, output_directory):
        os.makedirs(output_directory, exist_ok=True)
        for filename in os.listdir(input_directory):
            file_path = os.path.join(input_directory, filename)
            output_file_path = os.path.join(output_directory, os.path.splitext(filename)[0] + ".jpg")
            
            if filename.lower().endswith(".heic"):
                img = self.convert_heic_to_image(file_path)
            elif filename.lower().endswith(".pdf"):
                images = Image.open(file_path).convert("RGB")
                images.save(output_file_path, "JPEG")
                continue
            else:
                img = Image.open(file_path)
            
            img = img.convert("RGB")  # Convert RGBA to RGB
            img.save(output_file_path, "JPEG")
            img.close()

    def remove_background(self, input_directory):
        for filename in os.listdir(input_directory):
            if filename.lower().endswith(".jpg"):
                file_path = os.path.join(input_directory, filename)
                output_file_path = file_path  # Overwrite the same file
                
                input_image = Image.open(file_path)
                output_image = remove(input_image)
                output_image = output_image.convert("RGB")  # Ensure image is in RGB mode
                output_image.save(output_file_path)
                input_image.close()

    def flip_images(self, input_directory):
        for filename in os.listdir(input_directory):
            if filename.lower().endswith(".jpg"):
                file_path = os.path.join(input_directory, filename)
                img = Image.open(file_path)
                flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
                flipped_img.save(file_path)
                img.close()

    def preprocess_image(self, image_path):
        image = Image.open(image_path)
        return self.transform(image).unsqueeze(0).to(self.device)

    def predict(self, image_tensor):
        with torch.no_grad():
            output = self.model(image_tensor)
            probabilities = F.softmax(output, dim=1)
        return probabilities[0][1].item()  # Rheumatoid arthritis class probability

    def detect_rheumatoid_arthritis(self, right_hand_dir, left_hand_dir):
        self.convert_to_jpg(right_hand_dir, right_hand_dir)
        self.convert_to_jpg(left_hand_dir, left_hand_dir)
        
        self.remove_background(right_hand_dir)
        self.remove_background(left_hand_dir)
        
        self.flip_images(left_hand_dir)
        
        right_hand_images = [img for img in os.listdir(right_hand_dir) if img.lower().endswith(".jpg")]
        left_hand_images = [img for img in os.listdir(left_hand_dir) if img.lower().endswith(".jpg")]

        if not right_hand_images:
            raise ValueError("右手の画像が存在しません。")
        if not left_hand_images:
            raise ValueError("左手の画像が存在しません。")

        right_hand_results = [self.predict(self.preprocess_image(os.path.join(right_hand_dir, img))) for img in right_hand_images]
        left_hand_results = [self.predict(self.preprocess_image(os.path.join(left_hand_dir, img))) for img in left_hand_images]

        right_hand_avg_prob = sum(right_hand_results) / len(right_hand_results)
        left_hand_avg_prob = sum(left_hand_results) / len(left_hand_results)

        return {"right_hand": right_hand_avg_prob, "left_hand": left_hand_avg_prob}

# 使用例
detector = RheumatoidArthritisDetector(model_checkpoint="/Users/hanaokaryousuke/flaskbook/apps/data/model.pth")
result = detector.detect_rheumatoid_arthritis(
    right_hand_dir="/Users/hanaokaryousuke/flaskbook/apps/data/pictures/image_righthand",
    left_hand_dir="/Users/hanaokaryousuke/flaskbook/apps/data/pictures/image_lefthand"
)
print(result)