from ..helpers import MDict
from ..logger import logger
from ..nodes import AbstractNode

import re

from docx.styles.style import _NumberingStyle
from docxtpl import RichText
from mistletoe.block_token import List

class ListNode(AbstractNode,tokenClass = List):
	generatedListNumId = 28004
	BULLET_STYLE = "bulletList"
	styles = {
		BULLET_STYLE: "mddotlistbullet",
	}

	bulletListNumId = None

	rawxml = """<w:p><w:pPr><w:numPr><w:ilvl w:val="%s"/><w:numId w:val="%s"/></w:numPr></w:pPr>%s</w:p>"""

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
		style = self.tplStyles[self.BULLET_STYLE]
		if style:
			ListNode.bulletListNumId = re.search(r'<w:numId w:val="([0-9]+)"/>',style.element.xml).group(1)
			logger.debug("Bullet List Style found : %s" % (self.bulletListNumId))
		else:
			# Can't find style, fallback to default order docx list
			# TODO : add the bullet list inside templace if not found.
			self.order = True 
			ListNode.bulletListNumId = -1
			logger.warning("Bullet List Style (%s) not found." % (style))

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
					xml += self.rawxml % (ilvl,numId,tmpXml)

		if self.order and ilvl==0:
			# Need to restart index for an ordered list
			ListNode.generatedListNumId += 1

		return MDict({'xml':xml})
