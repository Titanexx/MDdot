from ..helpers import MDict
from ..nodes import AbstractNode, TextNode

from docxtpl import RichText
from mistletoe.block_token import Paragraph

class ParagraphNode(AbstractNode,tokenClass=Paragraph):
	rawxml = """<w:p>%s%s</w:p>"""

	def __init__(self, block, parent=None, children=[]):
		super().__init__(block, parent, children)
		self.data = []
		for e in block.children: 
			TextNode(e,self)

	def getText(self):
		return ''.join([c.getText() for c in self.children])

	def generate(self):
		rt = RichText()
		for e in self.children:
			e.generate(rt)
		
		return MDict({'xml': (self.rawxml % (self.getStyleById(),rt.xml))})

