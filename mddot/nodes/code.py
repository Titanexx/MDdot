from nodes import ParagraphNode
from mistletoe.block_token import CodeFence

class CodeNode(ParagraphNode, tokenClass=CodeFence):
	rawxml = """<w:p><w:pPr><w:pStyle w:val="mddotblockcode"/></w:pPr>%s</w:p>"""
	
	def __init__(self, block, parent=None, children=[]):
		super().__init__(block, parent, children)
		self.language = block.language

		# Need some clean \n
		self.data[-1].text[-1] = self.data[-1].text[-1].strip()