from ..helpers import MDict
from ..nodes import AbstractNode, TextNode

import json
import re

from docxtpl import RichText
from mistletoe.block_token import Heading

getHStyle = lambda l: "H%s" % l

class HeaderNode(AbstractNode, tokenClass=Heading):
	# It's mandatory to use them as identifier inside the docx template

	# If we have more than one child node, we have to add parapgrah as a title style need to be a paragraph style in Word.
	headerxml= '</w:t></w:r></w:p><w:p><w:pPr><w:pStyle w:val="%s"/></w:pPr>%s</w:p><w:p><w:r><w:t>'

	styles = {
		getHStyle(1) : "mddotheader1",
		getHStyle(2) : "mddotheader2",
		getHStyle(3) : "mddotheader3",
		getHStyle(4) : "mddotheader4",
		getHStyle(5) : "mddotheader5",
		getHStyle(6) : "mddotheader6",
	}

	def __init__(self, block, parent=None, children=[]):
		super().__init__(block, parent, children)
		self.level = block.level
		self.contents = []

		for e in block.children: 
			# self.contents.append(TextNode(e,options={'style': self.styles[getHStyle(self.level)]}))
			self.contents.append(TextNode(e))
		self.content = ''.join([c.getTextForId() for c in self.contents])
		self._id = re.sub(r'[^a-z0-9]+', '', self.content.lower())
		if not self._id:
			logger.error("A header can't be empty. You need at least one caracter (not in link).")

	def __str__(self):
		return "Header %s : %s" % (self.level, self.id)

	def generate(self):
		context = MDict()

		rt = RichText()
		for c in self.contents:
			c.generate(rt)

		context["_full_xml"] = (self.headerxml % (self.styles[getHStyle(self.level)],rt.xml))

		count_keys = {}
		for child in self.children:
			childContext = child.generate()
			for k,v in childContext.items():
				if k not in context:
					# First paragraph no need to merge
					context[k] = v
					count_keys[k] = 0
					if k == "xml":
						context["_full_xml"] += v
					if k not in ["properties"] and "_full_xml" in v:
						context["_full_xml"] += v["_full_xml"]
				else:
					if k == "xml":
						context[k] += v
						context["_full_xml"] += v
					elif k == "table":
						if type(context[k]) in [dict,MDict]:
							# Create the tables endpoint if there are more than 1 table
							context["tables"] = [context[k]]
						context["tables"].append(v)
					else:
						#Change key if there is already the same sub header inside context
						count_keys[k] += 1
						k = "%s_%s" % (k,count_keys[k])
						context[k] = v
					if k not in ["properties"] and "_full_xml" in v:
						context["_full_xml"] += v["_full_xml"]

		context["_header_xml"] = (self.headerxml % (self.styles[getHStyle(self.level)],rt.xml))

		return MDict({self._id:context})