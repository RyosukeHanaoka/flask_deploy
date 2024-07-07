import os
from PIL import Image, ImageOps
import fitz  # PyMuPDF
import pyheif  # PyHEIF
import torch
from torchvision import transforms as T
import matplotlib.pyplot as plt
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

class Detr:
    def __init__(self):
        # 必要なパスを設定
        self.input_right_pre_path = '/Users/hanaokaryousuke/flaskbook/apps/data/pictures/xpright'
        self.input_left_pre_path = '/Users/hanaokaryousuke/flaskbook/apps/data/pictures/xpleft'
        self.output_right_pre_path = '/Users/hanaokaryousuke/flaskbook/apps/data/pictures/xpright_post'
        self.output_left_pre_path = '/Users/hanaokaryousuke/flaskbook/apps/data/pictures/xpleft_post'
        self.input_right_path = '/Users/hanaokaryousuke/flaskbook/apps/data/pictures/xpright_post'
        self.input_left_path = '/Users/hanaokaryousuke/flaskbook/apps/data/pictures/xpleft_post'
        #self.output_right_path = '/content/drive/MyDrive/xpright_post/'
        #self.output_left_path = '/content/drive/MyDrive/xpleft_post/'
        self.output_right_cropped_path = '/Users/hanaokaryousuke/flaskbook/apps/data/pictures/xpright_cropped'
        self.output_left_cropped_path = '/Users/hanaokaryousuke/flaskbook/apps/data/pictures/xpleft_cropped'

        # チェックポイントのクラス数を確認
        self.checkpoint_path ='/Users/hanaokaryousuke/flaskbook/apps/data/checkpoint.pth'
        checkpoint = torch.load(self.checkpoint_path, map_location='cpu')
        num_classes = checkpoint['model']['class_embed.weight'].shape[0]

        # モデルのロード
        self.model = torch.hub.load('facebookresearch/detr', 'detr_resnet50', pretrained=False, num_classes=7)
        self.model.load_state_dict(checkpoint['model'], strict=False)
        self.model.eval()

        # カラーマップとクラス名の定義
        self.COLORS = ["blue", "green", "red", "cyan", "magenta", "yellow", "black"]
        self.finetuned_classes = ['N/A', 'wrist', 'MCP1st', 'MCPs', 'IP', 'PIPs', 'DIPs']

        # 画像変換の定義
        self.transform = T.Compose([
            T.Resize(800),
            T.ToTensor(),
        ])

    def convert_to_png(self, input_path, output_path):
        for img_name in os.listdir(input_path):
            img_path = os.path.join(input_path, img_name)
            base_name, ext = os.path.splitext(img_name)

            # 拡張子の正規化
            ext = ext.lower()
            
            # 出力ファイル名を設定
            output_file_name = f"{base_name}.png"
            output_file_path = os.path.join(output_path, output_file_name)

            if ext in ['.jpg', '.jpeg', '.png']:
                img = Image.open(img_path)
                img.save(output_file_path)

            elif ext == '.pdf':
                pdf_document = fitz.open(img_path)
                for page_num in range(pdf_document.page_count):
                    page = pdf_document.load_page(page_num)
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    page_output_path = os.path.join(output_path, f"{base_name}_page{page_num}.png")
                    img.save(page_output_path)

            elif ext == '.heic':
                heif_file = pyheif.read(img_path)
                img = Image.frombytes(
                    heif_file.mode, 
                    heif_file.size, 
                    heif_file.data, 
                    "raw", 
                    heif_file.mode, 
                    heif_file.stride,
                )
                img.save(output_file_path)

            else:
                print(f"Unsupported file format: {ext}")

    def box_cxcywh_to_xyxy(self, x):
        x_c, y_c, w, h = x.unbind(1)
        b = [(x_c - 0.5 * w), (y_c - 0.5 * h),
             (x_c + 0.5 * w), (y_c + 0.5 * h)]
        return torch.stack(b, dim=1)

    def rescale_bboxes(self, out_bbox, size):
        img_w, img_h = size
        b = self.box_cxcywh_to_xyxy(out_bbox)
        b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
        return b

    def plot_results(self, pil_img, prob=None, boxes=None):
        plt.figure(figsize=(16,10))
        plt.imshow(pil_img)
        ax = plt.gca()
        colors = self.COLORS * 100
        if prob is not None and boxes is not None:
            for p, (xmin, ymin, xmax, ymax), c in zip(prob, boxes.tolist(), colors):
                ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                           fill=False, color=c, linewidth=3))
                cl = p.argmax()
                text = f'{self.finetuned_classes[cl]}: {p[cl]:0.2f}'
                ax.text(xmin, ymin, text, fontsize=15,
                        bbox=dict(facecolor='yellow', alpha=0.5))
        plt.axis('off')
        plt.show()

    def crop_and_save(self, img, boxes, classes, output_base_path, img_name):
        for idx, (box, cls) in enumerate(zip(boxes.tolist(), classes)):
            xmin, ymin, xmax, ymax = map(int, box)
            cropped_img = img.crop((xmin, ymin, xmax, ymax))
            class_name = self.finetuned_classes[cls.argmax()]

            # クラスごとのディレクトリを作成
            class_dir = os.path.join(output_base_path, class_name)
            os.makedirs(class_dir, exist_ok=True)

            # 画像を保存
            base_name, ext = os.path.splitext(img_name)
            if ext.lower() not in ['.jpg', '.jpeg', '.png']:
                ext = '.png'
            cropped_img.save(os.path.join(class_dir, f"{base_name}_{class_name}_{idx}{ext}"))

    def run_workflow(self, my_image, output_base_path, img_name):
        if my_image.mode == 'L':
            my_image = my_image.convert('RGB')

        img = self.transform(my_image).unsqueeze(0)

        outputs = self.model(img)
        for threshold in [0.9, 0.7]:
            probas_to_keep, bboxes_scaled = self.filter_bboxes_from_outputs(outputs, my_image.size, threshold=threshold)
            self.plot_results(my_image, probas_to_keep, bboxes_scaled)
            self.crop_and_save(my_image, bboxes_scaled, probas_to_keep, output_base_path, img_name)

    def filter_bboxes_from_outputs(self, outputs, image_size, threshold=0.7):
        probas = outputs['pred_logits'].softmax(-1)[0, :, :-1]
        keep = probas.max(-1).values > threshold

        bboxes_scaled = self.rescale_bboxes(outputs['pred_boxes'][0, keep], image_size)
        return probas[keep], bboxes_scaled

    def process_images(self, input_path, cropped_output_path, flip=False):
        for img_name in os.listdir(input_path):
            img_path = os.path.join(input_path, img_name)
            img = Image.open(img_path)

            if flip:
                img = ImageOps.mirror(img)

            self.run_workflow(img, cropped_output_path, img_name)

            # ファイル名の拡張子を修正して保存
            #base_name, ext = os.path.splitext(img_name)
            #if ext.lower() not in ['.jpg', '.jpeg', '.png']:
                #ext = '.png'
            #img.save(os.path.join(output_path, base_name + ext))

    def process_all_images(self):
        self.process_images(self.input_right_path, self.output_right_cropped_path, flip=False)
        self.process_images(self.input_left_path,self.output_left_cropped_path, flip=True)

# インスタンスの作成と処理の実行
detr_instance = Detr()

# まず、画像をPNGに変換する
detr_instance.convert_to_png(detr_instance.input_right_pre_path, detr_instance.output_right_pre_path)
detr_instance.convert_to_png(detr_instance.input_left_pre_path, detr_instance.output_left_pre_path)

# その後、画像を処理する
detr_instance.process_all_images()