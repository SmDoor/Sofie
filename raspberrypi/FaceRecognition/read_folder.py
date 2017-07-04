import sys
import os
from skimage import io
import re

def read_folder(folder_name):
	images = {}
	for file_name in os.listdir(folder_name):
		match = re.match('.+\\.', file_name)
		if match is not None:
			name = file_name[:match.end()-1]
			name = re.sub('_', ' ', name)
			images[name] = io.imread(os.path.join(
					folder_name, file_name))
	return images		
