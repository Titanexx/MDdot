from ..helpers import MDict
from ..nodes import ParagraphNode
from ..logger import logger

from docxtpl import RichText
from mistletoe.block_token import CodeFence
from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter, RtfFormatter
from pygments.formatter import Formatter

class RTFormatter(Formatter):
	def __init__(self, rt, **options):
		Formatter.__init__(self, **options)
		self.rt = rt

	def format(self, tokensource, out):
		oldOptions = {}
		values = ''
		for ttype, value in tokensource:
			while not self.style.styles_token(ttype) and ttype.parent:
				ttype = ttype.parent
			style = self.style.style_for_token(ttype)
			options = {}
			if style['bgcolor']:
				# Maybe TODO True bgcolor
				options['highlight'] = style['bgcolor']
			if style['color']:
				options['color'] = style['color']
			if style['bold']:
				options['bold'] = True
			if style['italic']:
				options['italic'] = True
			if style['underline']:
				options['underline'] = 'single'
			if style['border']:
				# TODO if necessary
				pass
			if options == oldOptions:
				values += value
			else:
				self.rt.add(values,**(oldOptions))
				oldOptions = options
				values = value
		self.rt.add(values.rstrip(),**(oldOptions))

class CodeNode(ParagraphNode, tokenClass=CodeFence):
	BLOCK_CODE = "blockCode"
	styles = {
		BLOCK_CODE : "mddotblockcode",
	}
	
	rawxml = """<w:p><w:pPr><w:pStyle w:val='"""+styles[BLOCK_CODE]+"""'/></w:pPr>%s</w:p>"""
	
	def __init__(self, block, parent=None, children=[]):
		super().__init__(block, parent, children)
		self.hasLanguage = False
		if block.language:
			try:
				self.language = block.language
				self._lexer = get_lexer_by_name(self.language)
				self.hasLanguage = True
				logger.debug("Found a block code with %s inside." % self.language)
			except ClassNotFound as e:
				logger.warning("%s lexer not found inside pygments." % block.language)
			except Exception as e:
				raise e
		# Need some clean \n
		self.children[-1].text[-1] = self.children[-1].text[-1].strip()

	def generate(self):
		rt = RichText()
		if self.hasLanguage:
			formatter = RTFormatter(rt)
			highlight(self.getText(),self._lexer,formatter)
		else:
			for e in self.children:
				e.generate(rt)
		
		return MDict({'xml': self.rawxml % rt.xml})
