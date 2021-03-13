from anytree import NodeMixin
from logger import logger
from docxtpl import RichText, InlineImage

class AbstractNode(NodeMixin):
	template = None
	docxTemplate = None
	mdFilename = None
	
	images = {}
	tables = {}
	
	classByToken = {}
	
	def __init_subclass__(cls, tokenClass=None, **kwargs):
		if tokenClass:
			super().__init_subclass__(**kwargs)
			logger.info("Register %s for %s" % (tokenClass,cls))
			if tokenClass not in cls.classByToken: 
				cls.classByToken[tokenClass] = [cls]
			else: 
				cls.classByToken[tokenClass].append(cls)

	@classmethod
	def createFromToken(cls,token,parent):
		tokenType = type(token)
		good_class = cls.classByToken['none'][0]
		if not tokenType in cls.classByToken:
			logger.warning("Ignore %s because it's not implemented." % tokenType)
		else:
			for c in cls.classByToken[tokenType]:
				if c.condition(token,parent):
					good_class = c
			logger.debug("Generate %s for %s with parent %s" % (good_class,tokenType,parent))

		return good_class(token,parent)

	@classmethod
	def finalizeImages(cls,tpl):
		for id,img in cls.images.items():
			logger.debug("Load image %s inside %s." % (img,tpl))
			img['image'] = InlineImage(tpl,img['src'])

	@staticmethod
	def condition(block,parent):
		return True

	@staticmethod
	def getBlockType(block):
		return  block.__class__.__name__
	
	def __init__(self, block=None, parent=None, children=[]):
		super().__init__()
		self._block = block
		self.parent = parent
		self.children = children

	def __str__(self):
		return self.__class__.__name__

	def generate(self):
		logger.warning("%s must implement generate method" % self.__class__)
		return {}