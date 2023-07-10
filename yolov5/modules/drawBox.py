import os
import matplotlib

# Settings
RANK = int(os.getenv('RANK', -1))
matplotlib.rc('font', **{'size': 11})
matplotlib.use('Agg')  # for writing to files only

class Colors:
	def __init__(self):
		hex = ('FF3838', 'FF9D97', 'FF701F', 'FFB21D', 'CFD231', '48F90A', '92CC17', '3DDB86', '1A9334', '00D4BB',
			   '2C99A8', '00C2FF', '344593', '6473FF', '0018EC', '8438FF', '520085', 'CB38FF', 'FF95C8', 'FF37C7')
		self.palette = [self.hex2rgb('#' + c) for c in hex]
		self.n = len(self.palette)

	def __call__(self, i, bgr=False):
		c = self.palette[int(i) % self.n]
		return (c[2], c[1], c[0]) if bgr else c
	@staticmethod
	def hex2rgb(h):
		return tuple(int(h[1 + i:1 + i + 2], 16) for i in (0, 2, 4))