import os
import torchvision
import torchvision.transforms as transforms
import torch
import numpy as np
import argparse
from PIL import Image

def crop_img(x):
    W, H = x.size
    D = min(W, H)
    x = x.crop(((W-D)/2, (H-D)/2, (W+D)/2, (H+D)/2))
    x = x.resize((256, 256))
    return x

def blur(x, y, blur_edge=5):
	tmp_x = x.copy()
	for i in range(x.shape[0]):
		for j in range(x.shape[1]):
			if (y[i, j] == 255):
				tmp =  np.zeros(3)
				tmp_cnt = 0
				for k in range(max(0, i-blur_edge), min(x.shape[0], i+blur_edge+1)):
					for l in range(max(0, j-blur_edge), min(x.shape[1], j+blur_edge+1)):
						tmp += tmp_x[k, l]
						tmp_cnt += 1
				x[i, j] = np.array(tmp/tmp_cnt, dtype='uint8')
	return x

def blur_img(img):
	parser = argparse.ArgumentParser()
	parser.add_argument('--device', default=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu'))
	parser.add_argument('--save_path', default='./model.pth')
	parser.add_argument('--n_classes', default=2)
	parser.add_argument('--img_folder', default="img_folder")

	args = parser.parse_args()

	print("-----------config")
	for arg in vars(args):
		print("{:} : {:}".format(arg, getattr(args, arg)))
	print("-----------------")

	# load model
	net = torchvision.models.segmentation.deeplabv3_resnet101(pretrained=True, progress=True, num_classes=21, aux_loss=True)
	net.load_state_dict(torch.load(args.save_path, map_location=torch.device('cpu')))
	net.to(args.device)
	print("model loaded")

	# crop_256 and ToTensor
	img = crop_img(img)
	Totensor = transforms.ToTensor()
	img_arr = Totensor(img)

	# segment image
	inputs = torch.cat([img_arr.to(args.device).unsqueeze(0), img_arr.to(args.device).unsqueeze(0)], dim=0)
	outputs = net(inputs)["out"]
	predicts = torch.max(outputs, dim=1)[1]
	print("segmentation finished")

	# if (predicts==15) 1 else 0
	predicts[predicts!=15] = 0
	predicts[predicts==15] = 1

	for j in range(outputs.shape[0]):
		out_arr = np.array(torch.max(outputs[j], dim=0)[1].cpu(), dtype='uint8')
		out_arr[out_arr!=15] = 0
		out_arr[out_arr==15] = 255
		# out_img = Image.fromarray(out_arr, mode='L')

	# blur image
	img_arr = np.array(img)
	out_arr = np.array(out_arr)
	img_arr = blur(img_arr, out_arr)
	print("blur finished")

	img = Image.fromarray(img_arr)
	return img
