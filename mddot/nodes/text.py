from nodes import AbstractNode
from docxtpl import RichText, InlineImage
from html import escape

from logger import logger
from helpers import getBlockType

import os
import copy

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

	def __init__(self, block, parent=None, children=[]):
		super().__init__(block, parent, children)
		self.options = []
		self.text = []

		self.parse(self._block,{})

	def __str__(self):
		return "Text Node : %s | %s" % (repr(self.text), self.options)

	def _addText(self, text, options):
		self.options.append(options)
		self.text.append(text)

	def _setImage(self,block):
		# If all is ok, image otken must be alone in paragraph token
		captionxml = """</w:p><w:p><w:pPr><w:pStyle w:val="%s"/></w:pPr>"""
		
		key = 'img_'+str(len(self.images))
		imgId = 'images.%s.img' %(key)

		self._addText("{{ %s }}" % (imgId),{})
		if block.title:
			rt = RichText()
			rt.xml = captionxml % (self.styles[self.CAPTION],escape(block.title))
			self._addText(rt,{})
		elif block.children:
			rt = RichText()
			rt.xml = captionxml % (self.styles[self.CAPTION])
			self._addText(rt,{})
			self._parseChild(block,{'style':self.styles[self.CAPTION]})

		src = os.path.join(self.files.ressourcesPath,block.src)
		self.images[key] = {'src':src,'title':block.title,'id':imgId}

	def _parseChild(self,block,options):
		for childBlock in block.children:
			self.parse(childBlock,copy.deepcopy(options))

	def parse(self, block, options):
		blockType = getBlockType(block)

		if blockType not in self.SUPPORTED_TYPES:
			logger.error("%s must be implemented inside TextNode (or your md is too complicated ;))" % blockType)
		elif blockType == self.RAWTEXT:
			self._addText(block.content,options)
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
				self._addText(block.target,options)
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