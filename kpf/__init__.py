from kpf.patch import Patch,Record,sha256

def parse(text):
	patches = Patch.fromText(text)
	return patches

def parseFile(filename):
	with open(filename) as f:
		return parse(f.read().strip())
