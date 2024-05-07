import albumentations as A
import cv2
import random
import os

for _ in range(1000):
    # 每次循环随机选择一组增强方法
    random_augmentations = [
        A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3, p=1),
        A.RandomRotate90(p=1),
        A.GaussianBlur(p=1), # 高斯模糊
        A.GaussNoise(var_limit=(400, 450),mean=0,p=1),  # 高斯噪声
        A.Rotate(limit=45, interpolation=0, border_mode=0, p=1),
        A.Rotate(limit=30, interpolation=0, border_mode=0, p=1),
        A.Rotate(limit=75, interpolation=0, border_mode=0, p=1),
        A.Rotate(limit=120, interpolation=0, border_mode=0, p=1),
        A.RGBShift(r_shift_limit=50, g_shift_limit=50, b_shift_limit=50, p=1),
        A.ColorJitter(p=1),  # 随机改变图像的亮度、对比度、饱和度、色调
        A.Downscale(p=1),  # 随机缩小和放大来降低图像质量
        A.HorizontalFlip(p=0.5), # 水平翻转

        A.Emboss(p=0.2),  # 压印输入图像并将结果与原始图像叠加
        A.CLAHE(clip_limit=2.0, tile_grid_size=(4, 4), p=0.8),  # 直方图均衡
        A.Equalize(p=0.8),  # 均衡图像直方图
        A.ChannelShuffle(p=0.3),# 随机排列通道
        
        A.RandomFog(fog_coef_lower=0.1),
        A.RandomRain(p=0.3), 
        A.RandomSnow(),

    ]
    # 随机选择增强方法
    selected_augmentations = random.sample(random_augmentations, k=1) # k = min(len(random_augmentations), num_augmentations)
    # 创建增强策略
    transform = A.Compose(selected_augmentations, 
                          bbox_params=A.BboxParams(format='yolo',label_fields=['class_names']))

'''p 表示调整的概率'''

#  多文件处理

image_path = "/Users/rl/Documents/PhD_student/Untitled_Folder/CPLID/Defective_Insulators/images/"
bboxes_path = "/Users/rl/Documents/PhD_student/Untitled_Folder/CPLID/Defective_Insulators/labels/defect_txt/"

# 获取txt
def getcls_bbox(yolofile):
    # for yolofile in os.listdir(bboxes_path):
    with open(bboxes_path + yolofile,'r') as f:
        # f = open('test.txt','r')
        lines = f.readlines()
        # print(lines)
    # sents = []
    for line in lines:
        line = line.strip() # 消除空行
        tokens = line.split(' ') # 消除空格
        # print(tokens)
    #     for token in tokens:
    #         if len(token) > 0:
    #             sents.append(token)
    # print(sents)
        for i in range(5):
            class_names = [tokens[0]]
            x_center = float(tokens[1])
            y_center = float(tokens[2])
            w = float(tokens[3])
            h = float(tokens[4])
            bboxes = [x_center,y_center,w,h]
    return class_names,bboxes


# image_list = []
img_save_path = '/Users/rl/Documents/PhD_student/Untitled_Folder/CPLID/Defective_Insulators/albuimg/'
txt_save_path = '/Users/rl/Documents/PhD_student/Untitled_Folder/CPLID/Defective_Insulators/albutxt/'
for i in range(2):
    for filename in os.listdir(image_path):
        # 获取文件名前缀 的 2个方法
        os.path.splitext(filename)[0]
        prefix, _ = filename.split('.', 1)
        # print(prefix)

        if filename.endswith(".jpg") or filename.endswith(".png"):
            image = cv2.imread(os.path.join(image_path, filename))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # image_list.append(image)
            class_names,bboxes = getcls_bbox(prefix + '.txt')
            bboxes = [bboxes]
            # print(class_names)
            # print(bboxes)
            transformed = transform(image=image,bboxes=bboxes,class_names=class_names)
            transformed_image = transformed["image"]
            transformed_bboxes = transformed['bboxes']
            t_bbox = list(transformed_bboxes[0])
            # print(t_bbox)
            cv2.imwrite(img_save_path + prefix + '_' + str(i) + 'albu.jpg',transformed_image)
            albu_txt = open(txt_save_path + prefix + '_' + str(i) + 'albu.txt' ,'w')
            albu_txt.write(str(class_names[0])+" "+str(t_bbox[0])+" "+str(t_bbox[1])+" "+str(t_bbox[2])+" "+str(t_bbox[3])+'\n')

        albu_txt.close()







#####  单文件
#     # Declare an augmentation pipeline
# transform = A.Compose([
#     # A.RandomCrop(width=256, height=256),
#     A.HorizontalFlip(p=0.5),
#     A.RandomBrightnessContrast(p=0.2),
#     # A.RandomFog(fog_coef_lower=0.1),
#     A.RandomRain(p=0.3), 
#     # A.RandomSnow(),

#     A.Blur(p=0.01),
#     A.MedianBlur(p=0.01),
#     A.ToGray(p=0.01),
#     A.CLAHE(p=0.01),
#     A.RandomBrightnessContrast(p=0.0),
#     A.RandomGamma(p=0.0),
#     A.ImageCompression(quality_lower=75, p=0.0),
# ],
#     bbox_params=A.BboxParams(format='yolo',label_fields=['class_names']),
# )

# # Read an image with OpenCV and convert it to the RGB colorspace
# image = cv2.imread("/Users/rl/Documents/PhD_student/Untitled_Folder/image/000.jpg")
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# # Augment an image
# transformed = transform(image=image)
# transformed_image = transformed["image"]

# cv2.imwrite('albu.jpg',transformed_image)