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
		self.assertEqual(patches[0].name,"NOP the check for XYZ encoding")
		self.assertIsNone(patches[0].hash)
		self.assertEqual(patches[0].records[0].address,0x3033)
		self.assertEqual(patches[0].records[0].value,0)
	def test_patch_text(self):
		patch1 = kpf.Patch("Test case")
		patch1.records=[]
		patch1.records.append(kpf.Record.fromLine("0002=02"))
		self.assertEqual(patch1.text,".patch\n.name Test case\n00000002=02\n.endpatch")

if __name__=="__main__": unittest.main()
