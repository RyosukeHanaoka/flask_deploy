import os
import torch
from PIL import Image
from rembg import remove
from torchvision import transforms
import timm
#from .extensions import db
import torch.nn.functional as F
from pillow_heif import register_heif_opener
register_heif_opener()

class Vit:
    def __init__(self, model_checkpoint, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.load_model(model_checkpoint)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])
        self.jpeg_righthand_dir = "/Users/hanaokaryousuke/flask/apps/data/pictures/jpeg_righthand"
        self.jpeg_lefthand_dir = "/Users/hanaokaryousuke/flask/apps/data/pictures/jpeg_lefthand"

    def load_model(self, model_checkpoint):
        model = timm.create_model('vit_base_patch16_224.augreg_in21k', pretrained=False, num_classes=2)
        checkpoint = torch.load(model_checkpoint, map_location=self.device)
        model.load_state_dict(checkpoint)
        model.to(self.device)
        model.eval()
        return model

    def convert_heic_to_image(self, heic_path):
        # pillow_heifを使ってHEICファイルを読み込む
        image = Image.open('image.heic')
        return image

    def convert_to_jpg(self, file_path, output_directory):
        os.makedirs(output_directory, exist_ok=True)
        filename=os.path.basename(file_path)
        output_file_path = os.path.join(output_directory, os.path.splitext(filename)[0] + ".jpg")
        
        if filename.lower().endswith(".heic"):
            img = self.convert_heic_to_image(file_path)
        elif filename.lower().endswith(".pdf"):
            images = Image.open(file_path).convert("RGB")
            images.save(output_file_path, "JPEG")
        else:
            img = Image.open(file_path)
        
        img = img.convert("RGB")  # Convert RGBA to RGB
        img.save(output_file_path, "JPEG")
        img.close()
        return output_file_path

    def remove_background(self, file_path):
        output_file_path = file_path  # Output file path is the same as input file path       
        input_image = Image.open(file_path)
        output_image = remove(input_image)
        output_image = output_image.convert("RGB")  # Ensure image is in RGB mode
        output_image.save(output_file_path)
        input_image.close()
        return output_file_path

    def flip_images(self, file_path, output_directory):
        filename_base = os.path.splitext(os.path.basename(file_path))[0]
        output_file_path = os.path.join(output_directory, filename_base + "_flipped.jpg")
        img = Image.open(file_path)
        flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
        flipped_img.save(output_file_path)
        img.close()
        return output_file_path

    def preprocess_image(self, image_path):
        image = Image.open(image_path)
        return self.transform(image).unsqueeze(0).to(self.device)

    def predict(self, image_tensor):
        with torch.no_grad():
            output = self.model(image_tensor)
            probabilities = F.softmax(output, dim=1)
        return probabilities[0][1].item()  # Rheumatoid arthritis class probability

    def detect_rheumatoid_arthritis(self, right_hand_file, left_hand_file):
        jpeg_righthand=self.convert_to_jpg(right_hand_file, self.jpeg_righthand_dir)
        jpeg_lefthand=self.convert_to_jpg(left_hand_file, self.jpeg_lefthand_dir)
        
        removed_righthand=self.remove_background(jpeg_righthand)
        removed_lefthand=self.remove_background(jpeg_lefthand)
        
        flipped_lefthand=self.flip_images(removed_lefthand, os.path.dirname(removed_righthand))

        right_hand_result = self.predict(self.preprocess_image(removed_righthand))
        left_hand_result = self.predict(self.preprocess_image(flipped_lefthand))
        result=100*(right_hand_result+left_hand_result)/2
        
        # 結果をデータベースに保存
        #self.save_results_to_db(right_hand_result, left_hand_result, result)
        return right_hand_result, left_hand_result, result
