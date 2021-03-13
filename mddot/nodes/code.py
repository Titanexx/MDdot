from nodes import ParagraphNode
from docxtpl import RichText
from mistletoe.block_token import CodeFence

class CodeNode(ParagraphNode, tokenClass=CodeFence):
	BLOCK_CODE = "blockCode"
	styles = {
		BLOCK_CODE : "mddotblockcode",
	}
	
	rawxml = """<w:p><w:pPr><w:pStyle w:val='"""+styles[BLOCK_CODE]+"""'/></w:pPr>%s</w:p>"""
	
	def __init__(self, block, parent=None, children=[]):
		super().__init__(block, parent, children)
		self.language = block.language

		# Need some clean \n
		self.children[-1].text[-1] = self.children[-1].text[-1].strip()

	def generate(self):
		rt = RichText()
		for e in self.children:
			e.generate(rt)
			
		return {'xml': (self.rawxml % (rt.xml))}
