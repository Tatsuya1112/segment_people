from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import FieldStorage
import io
from PIL import Image
import torch
import numpy as np
from Segment import *

# load html file.
with open('index.html', mode='r') as f:
	index = f.read()
with open('next.html', mode='r') as f:
	next = f.read()

routes = []

def route(path, method):
	routes.append((path, method))

# add route setting.
route('/', 'index')
route('/index', 'index')
route('/next', 'next')
route('/img.png', 'img')
route('/img_blur.png', 'img_blur')

class HelloServerHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		_url = urlparse(self.path)
		if (_url.path == '/'):
			self.index()
		elif (_url.path == '/next'):
			self.next()
		elif (_url.path == '/img.png'):
			self.img()
		elif (_url.path == '/img_blur.png'):
			self.img_blur()
		else:
			self.error()

	def do_POST(self):
		form = FieldStorage(
			fp = self.rfile,
			headers = self.headers,
			environ = {'REQUEST_METHOD': 'POST'}
		)
		res = form['textfield'].value
		self.send_response(200)
		self.end_headers()

		##################################################
		# save input image
		img_from_byte = Image.open(io.BytesIO(res))
		img_from_byte.save('img_raw.png')

		# crop input image
		img_from_byte_crop = crop_img(img_from_byte)
		img_from_byte_crop.save('img.png')

		# blur person
		img_from_byte_blur = blur_img(img_from_byte)
		img_from_byte_blur.save('img_blur.png')
		##################################################

		img_arr = torch.tensor(np.array(img_from_byte))

		html = next.format(
			input_msg = '入力',
			output_msg = '出力',
			return_index = '画像の入力に戻る'
		)

		self.wfile.write(html.encode('utf-8'))
		return

	def index(self):
		self.send_response(200)
		self.end_headers()
		html = index.format(
			title='人にモザイクをかけます!',
			text='入力画像を選択して下さい'
		)
		self.wfile.write(html.encode('utf-8'))
		return

	# def next(self):
	# 	self.send_response(200)
	# 	self.end_headers()
	# 	html = next.format(
	# 		input_msg = '入力',
	# 		output_msg = '出力',
	# 		return_index = '画像の入力に戻る'
	# 	)
	# 	self.wfile.write(html.encode('utf-8'))
	# 	return

	def img(self):
		f = open('img.png', 'rb')
		self.send_response(200)
		self.send_header('Content-type', 'image/png')
		self.end_headers()
		self.wfile.write(f.read())
		f.close()
		return

	def img_blur(self):
		f = open('img_blur.png', 'rb')
		self.send_response(200)
		self.send_header('Content-type', 'image/png')
		self.end_headers()
		self.wfile.write(f.read())
		f.close()
		return

	def error(self):
		self.send_error(404, "CANNOT ACCESS!!")
		return

HTTPServer(('', 8000), HelloServerHandler).serve_forever()