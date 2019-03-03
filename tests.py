import unittest

import kpf

from textwrap import dedent
from kpf.patch import sha256

def readBinary(fn):
	with open(fn,"rb") as f:
		return bytearray(f.read())

class KPFTests(unittest.TestCase):
	def test_record_parse(self):
		r = kpf.Record.fromLine("00000002=02")
		self.assertEqual(type(r),kpf.Record)
		self.assertEqual(r.address,2)
		self.assertEqual(r.value,2)
		self.assertIsNone(r.compare)
	def test_patch_parse(self):
		patches = kpf.parse(dedent("""\
		.patch
		.name NOP the check for XYZ encoding
		00003033=0x00
		.endpatch"""))
		self.assertEqual(len(patches),1)
		patch = patches[0]
		print(patch)
		self.assertEqual(patch.name,"NOP the check for XYZ encoding")
		self.assertIsNone(patch.hash)
		self.assertEqual(patch.records[0].address,0x3033)
		self.assertEqual(patch.records[0].value,0)

if __name__=="__main__": unittest.main()
