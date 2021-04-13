from .logger import logger

from docx.shared import Twips
from jinja2 import Template
from lxml import etree


def doJinjaRender(tpl,context):
	t = Template(tpl)
	return t.render(context)

def getMarginFromStyle(style,side):
	margin = style._element.xpath('.//w:tblCellMar/w:%s/@w:w'%side)
	marginType = style._element.xpath('.//w:tblCellMar/w:%s/@w:type'%side)
	if not margin and not marginType and style.base_style:
		return getMarginFromStyle(style.base_style,side)
	if marginType[0] != 'dxa':
		logger.error("Ok, I don't manage this case. Open an issue : Margin type support %s" % marginType)
	return Twips(int(margin[0])) 

def getpPr(paragraph):
	res = ""
	pPr = paragraph._element.xpath('./w:pPr')
	if pPr :
		res = etree.tostring(pPr[0]).decode('utf-8')
		res = "<w:pPr"+res[res.find("><"):]
	return res

def getBlockType(block):
	return  block.__class__.__name__

def compareKeys(key1, key2):
	keys1 = key1.split('.')
	keys2 = key2.split('.')
	if len(keys1) != len(keys2):
		return False
	
	for i in range(len(keys1)):
		if keys1[i] != keys2[i] and keys2[i] != "*":
			return False
	return True

class MDict(dict):  # dicts take a mapping or iterable as their optional first argument
	INTERNALS = [
		"properties",
		"_full_xml", "xml",
		"_header_xml",
	]

	def items(self):
		return super().items()

	def mdItems(self):
		res = []
		for k,v in super().items():
			if not k.startswith('_') and k not in self.INTERNALS:
				res.append((k,v))
		return res
