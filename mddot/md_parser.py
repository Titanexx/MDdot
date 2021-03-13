from mistletoe.block_token import Heading, List, Table, Paragraph, CodeFence
from anytree import RenderTree

from logger import logger
from nodes import RootNode

class Parser():
	def __init__(self,md, template, mdFilename):
		self._md = md
		self._template = template
		self.tree = RootNode(mdFilename, template)

		self._parseMD()

	def _parseMD(self,):
		root = self.tree
		parent = root
		level = 0
		for b in self._md.children:
			typeB = type(b) 
			if typeB == Heading:
				if b.level == level:
					parent = RootNode.createFromToken(b,parent.parent)
				elif b.level > level:
					# Here, we take the assumption that the level heading is good, 
					# like 1, 1.1, 1.1.1, 1.2, 2, 2.1, 2.2, 2.2.1, 2.2.2, 2.2.2.1, 2.3, not like 1, 1.1.1, 1.2.
					level = b.level
					parent = RootNode.createFromToken(b,parent)
				elif b.level < level:
					for _ in range(0,level - b.level + 1):
						parent = parent.parent
					level = b.level
					parent = RootNode.createFromToken(b,parent)
			else:
				e = RootNode.createFromToken(b,parent)

	def generateDocx(self):
		return self.tree.generate()

	def finalize(self,tpl):
		self.tree.finalizeImages(tpl)

	def __str__(self):
		res = ""
		for pre, _, node in RenderTree(self.tree):
			treestr = u"%s%s" % (pre, node)
			res += treestr.ljust(8) + "\n"
		return res