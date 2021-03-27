import os
from copy import deepcopy

from nodes import AbstractNode
from logger import logger
from helpers import getBlockType, getMarginFromStyle

from PIL import Image
from docx.shared import Length
from docxtpl import RichText, InlineImage
from html import escape as escapeXML



class TextNode(AbstractNode, tokenClass='*'):
	INLINE_CODE = "inlineCode"
	LINK_STYLE = "link"
	CAPTION = "caption"
	styles = {
		INLINE_CODE: "mddottextinlinecode",
		LINK_STYLE:"mddottextlink",
		CAPTION:"mddottextcaption",
	}

	RAWTEXT = "RawText"
	STRONG = "Strong"
	EMPHASIS = "Emphasis"
	IMAGE = "Image"
	LINEBREAK = "LineBreak"
	STRIKETHROUGH = "Strikethrough"
	INLINECODE = "InlineCode"
	LINK = "Link"

	SUPPORTED_TYPES = [
		RAWTEXT,
		STRONG,
		EMPHASIS,
		IMAGE,
		LINEBREAK,
		STRIKETHROUGH,
		INLINECODE,
		LINK
	]

	# If all is ok, image otken must be alone in paragraph token
	captionxml = """</w:p><w:p><w:pPr><w:pStyle w:val="%s"/></w:pPr>"""

	def __init__(self, block, parent=None, children=[]):
		super().__init__(block, parent, children)
		self.options = []
		self.text = []

		self.parse(self._block,{})

	def getText(self):
		return ''.join(self.text)

	def __str__(self):
		return "Text Node : %s | %s" % (repr(self.text), self.options)

	def _addText(self, text, options):
		self.options.append(options)
		self.text.append(text)

	def _addXML(self,xml,options):
		rt = RichText()
		rt.xml = xml
		self._addText(rt,options)

	def _setImage(self, block):	
		src = os.path.join(self.files.ressourcesPath,block.src)
		p = self.files.getTplByKey(self.id)[0]

		if p:
			# Get docx margin values
			if "_Body" in str(type(p._parent)):
				section = p._parent._element.xpath(".//following::w:sectPr")[0]
				length=section.page_width - (section.right_margin + section.left_margin) 
			else:			
				rightMargin = getMarginFromStyle(p._parent._parent.style,'right')
				leftMargin = getMarginFromStyle(p._parent._parent.style,'left')
				length = Length(p._parent.width) - (rightMargin + leftMargin)

			# Get image size
			im = Image.open(src)
			width, height = im.size
			dpiWidth, dpiHeight = im.info['dpi']
			widthEmus = width / dpiWidth * Length._EMUS_PER_INCH
			heightEmus = height / dpiHeight * Length._EMUS_PER_INCH
			imgWidth = widthEmus
			# Change target width if needed.
			if widthEmus > length:
				imgWidth = length

			logger.debug("Load image %s inside %s." % (src,self.files.tplFilename))
			image = InlineImage(self.files.tpl,src,imgWidth)
		else:
			logger.warning("Inserting image in %s failed. Key is not found." % self.id)

		self._addXML(str(image)[12:-31],{})
		self._addXML(self.captionxml % (self.styles[self.CAPTION]),{})

		if block.title:
			self._addText(block.title,{'style':self.styles[self.CAPTION]})
		elif block.children:
			self._parseChild(block,{'style':self.styles[self.CAPTION]})
		
	def _parseChild(self,block,options):
		for childBlock in block.children:
			self.parse(childBlock,deepcopy(options))

	def parse(self, block, options):
		blockType = getBlockType(block)

		if blockType not in self.SUPPORTED_TYPES:
			logger.error("%s must be implemented inside TextNode (or your md is too complicated ;))" % blockType)
		elif blockType == self.RAWTEXT:
			self._addText(block.content, options)
		elif blockType == self.LINEBREAK:
			self._addText("\n",options)
		elif blockType == self.IMAGE:
			self._setImage(block)
		elif blockType == self.LINK:
			options['url_id'] = self.files.tpl.build_url_id(block.target)
			options['style'] = self.styles[self.LINK_STYLE]
			if block.children:
				self._parseChild(block,options)
			else:
				self._addText(block.target, options)
		elif blockType == self.STRONG:
			options['bold'] = True
			self._parseChild(block,options)
		elif blockType == self.EMPHASIS:
			options['italic'] = True
			self._parseChild(block,options)
		elif blockType == self.STRIKETHROUGH:
			options['strike'] = True
			self._parseChild(block,options)
		elif blockType == self.INLINECODE:
			options['style'] = self.styles[self.INLINE_CODE]
			self._parseChild(block,options)

	def generate(self,rt = None):
		if not rt:
			rt = RichText()
		for i in range(len(self.text)):
			logger.spam("TextNode generation (text | option) : (%s | %s)" % (repr(self.text[i]),self.options[i]))
			rt.add(self.text[i],**(self.options[i]))
		return rt