from . import helpers
from .logger import logger

import os
import re

from docxtpl import DocxTemplate
from mistletoe import Document

class Files():
	TMP_FILENAME = "temp.docx"

	def __init__(self,mdFilename,tplFilename,outFilename):
		self.tpl = None
		self.tplDocx = None
		self.keysTplCache = {}

		self.mdFilename = mdFilename
		with open(mdFilename,'r') as f:
			self.__rawMd = f.read()

		self.md = Document(self._rawMd)

		self.ressourcesPath = os.path.dirname(self.mdFilename)
		self.tplFilename = tplFilename
		self.outFilename = outFilename

		logger.verbose("Files : %s, %s, %s" % (mdFilename, tplFilename, outFilename))
	
	@property
	def _rawMd(self):
		return self.__rawMd

	@_rawMd.setter
	def _rawMd(self,_rawMd):
		self.__rawMd = _rawMd
		self.md = Document(self._rawMd)

	@property
	def tplFilename(self):
		return self._tplFilename

	@tplFilename.setter
	def tplFilename(self,tplFilename):
		self._tplFilename = tplFilename
		self.tpl = DocxTemplate(tplFilename)
		self.tplDocx = self.tpl.docx
		self._buildkeysTplCache()

	def _buildkeysTplCache(self):
		self.keysTplCache = {}
		keyRegex = re.compile(r'{{ (.*?)(\.(xml))? }}')
		forRegex = re.compile(r'\[[a-z]+\]')
		paragraphs = []
		for p in self.tplDocx.paragraphs:
			paragraphs.append(p)
		for t in self.tplDocx.tables:
			for r in t.rows:
				for c in r.cells:
					for p in c.paragraphs:
						if p not in paragraphs:
							# Avoid duplicate, should not append
							paragraphs.append(p)

		for p in paragraphs:
			key = keyRegex.search(p.text)
			if key:
				key = forRegex.sub(".*",key[1])
				if key[-1] == '.':
					key += '.'
				pPr = helpers.getpPr(p)
				self.keysTplCache[key] = (p,pPr)
		logger.debug("keysTplCache : %s" % self.keysTplCache.keys())
		logger.spam("keysTplCache : %s" % self.keysTplCache)

	def getTplByKey(self, key):
		if key in self.keysTplCache:
			# Raw id
			return self.keysTplCache[key]
		else:
			# handle for loop
			# Need jinja declaration as list not with items inside template 
			for tplKey in self.keysTplCache:
				if helpers.compareKeys(key,tplKey):
					return self.keysTplCache[tplKey]
			else:
				# _full_xml
				keys = key.split('.')
				for i in range(len(keys),-1,-1):
					tmpKey = '.'.join(keys[:i]+["_full_xml"])
					if tmpKey in  self.keysTplCache:
						return self.keysTplCache[tmpKey]

			return ("","")