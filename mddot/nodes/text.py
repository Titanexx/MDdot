from nodes import AbstractNode
from docxtpl import RichText, InlineImage
from logger import logger

import os
import copy


class TextNode(AbstractNode):
	INLINECODESTYLE = "mddottextinlinecode"

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

	ressourcePath = ""


	def __init__(self, block, parent=None, children=[]):
		super().__init__(block, parent, children)
		self.options = []
		self.text = []
		TextNode.ressourcePath = os.path.dirname(self.mdFilename)

		self.parse(self._block,{})

	def __str__(self):
		return "Text Node : %s | %s" % (repr(self.text), self.options)

	def _addText(self, text, options):
		self.options.append(options)
		self.text.append(text)

	def _setImage(self,block):
		idImage = 'image_'+str(len(self.images))
		
		text = "{{ %s.image }}" % (idImage)
		if block.title:
			text += "\n{{ %s.title }}" % (idImage)
		# Todo: add caption style support
		# Todo: support md style token
		self._addText(text,{})

		src = os.path.join(self.ressourcePath,block.src)
		self.images[idImage] = {'src':src,'title':block.title}

	def parse(self, block, options):
		def _parseChild(block,options):
			for childBlock in block.children:
				self.parse(childBlock,copy.deepcopy(options))

		blockType = self.getBlockType(block)

		if blockType not in self.SUPPORTED_TYPES:
			logger.error("%s must be implemented inside TextNode (or your md is too complicated ;))" % blockType)
		elif blockType == self.RAWTEXT:
			self._addText(block.content,options)
		elif blockType == self.LINEBREAK:
			self._addText("\n",options)
		elif blockType == self.IMAGE:
			self._setImage(block)
		elif blockType == self.LINK:
			options['url_id']=self.template.build_url_id(block.target)
			if block.children:
				_parseChild(block,options)
			else:
				self._addText(block.target,options)
		elif blockType == self.STRONG:
			options['bold'] = True
			_parseChild(block,options)
		elif blockType == self.EMPHASIS:
			options['italic'] = True
			_parseChild(block,options)
		elif blockType == self.STRIKETHROUGH:
			options['strike'] = True
			_parseChild(block,options)
		elif blockType == self.INLINECODE:
			options['style'] = self.INLINECODESTYLE
			_parseChild(block,options)

	def generate(self,rt = None):
		if not rt:
			rt = RichText()
		for i in range(len(self.text)):
			logger.spam("TextNode generation (text | option) : (%s | %s)" % (repr(self.text[i]),self.options[i]))
			rt.add(self.text[i],**(self.options[i]))
		return rt