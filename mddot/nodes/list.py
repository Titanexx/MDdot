from nodes import AbstractNode
from logger import logger
from docxtpl import RichText
from mistletoe.block_token import List
from docx.styles.style import _NumberingStyle
import re

class ListNode(AbstractNode,tokenClass = List):
	generatedListNumId = 28004 
	bulletListStyle = "mddotlistbullet"
	bulletListNumId = None

	xmllist = """<w:p><w:pPr><w:numPr><w:ilvl w:val="%s"/><w:numId w:val="%s"/></w:numPr></w:pPr>%s</w:p>"""

	def __init__(self, block, parent=None, children=[]):
		super().__init__(block, parent, children)

		self.order = block.start
		if not self.order and self.bulletListNumId is None:
			self._initBulletListStyle()

		self.data = []
		for item in block.children: 
			item_data = []
			for e in item.children:
				node = self.createFromToken(e,self)
				item_data.append(node)
			self.data.append(item_data)

	def _initBulletListStyle(self):
		for s in self.docxTemplate.styles:
			if s.style_id == self.bulletListStyle:
				ListNode.bulletListNumId = re.search(r'<w:numId w:val="([0-9]+)"/>',s.element.xml).group(1)
				logger.verbose("Bullet List Style (%s) found : %s" % (self.bulletListStyle,self.bulletListNumId))
				break
		else:
			# Can't find style, fallback to default order docx list
			# TODO : add the bullet list inside templace to use it
			self.order = True 
			ListNode.bulletListNumId = -1
			logger.warning("Bullet List Style (%s) not found." % (self.bulletListStyle))

	def generate(self, ilvl=0):
		if self.order:
			numId = self.generatedListNumId
		else:		
			numId = self.bulletListNumId

		xml = ""
		for item in self.data:
			for e in item:
				if type(e) == ListNode:
					# Nested List suppport
					tmpXml = e.generate(ilvl+1)['xml']
					xml += tmpXml
				else:
					# List item
					tmpXml = e.generate()['xml']
					tmpXml = tmpXml[5:-6]
					xml += self.xmllist % (ilvl,numId,tmpXml)

		if self.order and ilvl==0:
			# Need to restart index for an ordered list
			ListNode.generatedListNumId += 1

		return {'xml':xml}
