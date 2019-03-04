import re, copy
from kpf.fsm import FiniteStateMachine
from hashlib import sha256 as __sha256

def sha256(i):
	return __sha256(i).hexdigest()

class IncorrectRecordFormatException(Exception):
	def __init__(self,format,s):
		super(IncorrectRecordFormatException,self).__init__("Record {!r} is not in the {!r} format!".format(s,format))

class IncorrectFileHashException(Exception):
	def __init__(self):
		super(IncorrectFileHashException,self).__init__("Input hash is incorrect!")

class Record:
	"""A record. Has an address, value, and sometimes a compare value for run-time patching."""
	FORMAT = r"([0-9A-Fa-f]+)=(?:0x)?([0-9A-Fa-f]{2,2})"
	FORMAT_OUT = "{address:08X}={value:02X}"
	FIELDS = "address value".split()
	FORMAT_NAME = "Base record"
	def __init__(self,**kwargs):
		self.__dict__.update(kwargs)
	@classmethod
	def fromLine(cls,line):
		m = re.match(cls.FORMAT,line)
		if m is None: raise IncorrectRecordFormatException(cls.FORMAT_NAME,line)
		return cls(**({cls.FIELDS[x]: int(m.group(x+1),16) for x in range(len(cls.FIELDS))}))
	@property
	def compare(self):
		if hasattr(self,"_compare"): return self._compare
		return None
	def apply(self,b):
		if self.compare and self.compare!=b[self.address]: return
		b[self.address]=self.value
		return b
	@property
	def text(self):
		return self.FORMAT_OUT.format(**({x: getattr(self,x) for x in self.FIELDS+(["compare"] if hasattr(self,"_compare") else [])}))

def re_preproc(r):
	m = list(r)
	for match in re.finditer("<([^>]+)>",r):
		m[match.start():match.end()]=list(re.escape(match.group(1)))
	return "".join(m)

class PatchParser(FiniteStateMachine):
	PATCH_NAME = re.compile(re_preproc("<.>name (.+)"))
	PATCH_HASH = re.compile(re_preproc("<.>filehash ([0-9A-Fa-f]+)"))
	def __init__(self,pc):
		self.pc = pc
		self.state = "begin"
	def do_begin(self,line):
		if line==".patch":
			self.change("patch")
			self.patch = self.pc("")
	def do_patch(self,line):
		if line==".endpatch":
			self.change("begin")
			self.patch.records.sort(key=lambda x: x.address)
			return self.patch
		if self.PATCH_NAME.match(line):
			m = self.PATCH_NAME.match(line)
			self.patch.name=m.group(1)
		elif self.PATCH_HASH.match(line):
			m = self.PATCH_HASH.match(line)
			self.patch.hash=m.group(1)
		else:
			r = self.pc.parseRecord(line)
			if r is not None: self.patch.records.append(r)

class Patch:
	"""A patch. Contains Records."""
	RECORD_TYPES = [Record]
	def __init__(self,name,hash=None,records=[]):
		self.name = name
		self.hash = hash
		self.records = records
	@classmethod
	def fromText(self,text):
		lines = text.splitlines()
		patches = []
		fsm = PatchParser(self)
		for line in lines:
			ret = fsm.input(line)
			if ret is not None: patches.append(ret)
		return patches
	@classmethod
	def parseRecord(cls,line):
		for typ in cls.RECORD_TYPES:
			try:
				return typ.fromLine(line)
			except IncorrectRecordFormatException:
				pass
	def apply(self,b):
		if self.hash and sha256(b)!=self.hash: raise IncorrectFileHashException()
		b = copy.copy(b)
		for record in self.records:
			b = record.apply(b)
		return b
	@property
	def text(self):
		ret = [".patch"]
		ret.append(".name "+self.name)
		if self.hash: ret.append(".hash "+self.hash)
		for record in self.records:
			ret.append(record.text)
		ret.append(".endpatch")
		return "\n".join(ret)
