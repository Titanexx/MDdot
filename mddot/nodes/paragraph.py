from nodes import AbstractNode, TextNode
from docxtpl import RichText
from mistletoe.block_token import Paragraph

class ParagraphNode(AbstractNode,tokenClass=Paragraph):
	rawxml = "<w:p>%s</w:p>"

	def __init__(self, block, parent=None, children=[]):
		super().__init__(block, parent, children)
		
		self.data = []
		for e in block.children: 
			self.data.append(TextNode(e))

	def generate(self):
		rt = RichText()
		for e in self.data:
			e.generate(rt)
		return {'xml': self.rawxml % rt.xml}