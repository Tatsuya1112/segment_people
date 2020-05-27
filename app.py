from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import FieldStorage
import io
from PIL import Image
import torch
import numpy as np

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

class HelloServerHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		_url = urlparse(self.path)
		if (_url.path == '/'):
			self.index()
		elif (_url.path == '/next'):
			self.next()
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
		img_from_byte = Image.open(io.BytesIO(res))
		img_from_byte.save('img.png')
		##################################################

		img_arr = torch.tensor(np.array(img_from_byte))

		html = next.format(
			# message = 'you typed: ' + res,
			# message = 'you typed: ' + str(res),
			message = 'posted!',
			# data = form
			data = img_arr.shape
		)

		self.wfile.write(html.encode('utf-8'))
		return

	def index(self):
		self.send_response(200)
		self.end_headers()
		html = index.format(
			title='Hello',
			message='Form送信'
		)
		self.wfile.write(html.encode('utf-8'))
		return

	def next(self):
		self.send_response(200)
		self.end_headers()
		html = next.format(
			message = 'header data.',
			data=self.headers
		)
		self.wfile.write(html.encode('utf-8'))
		return

	def error(self):
		self.send_error(404, "CANNOT ACCESS!!")
		return

HTTPServer(('', 8000), HelloServerHandler).serve_forever()