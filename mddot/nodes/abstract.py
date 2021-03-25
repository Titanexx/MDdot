from logger import logger
import helpers

from anytree import NodeMixin

class AbstractNode( NodeMixin):
	files = None
	
	styles = {}
	tplStyles = {}
	
	images = {}
	tables = {}

	rawxml = ""
	
	classByToken = {}
	
	def __init_subclass__(cls, tokenClass=None, **kwargs):
		if tokenClass:
			super().__init_subclass__(**kwargs)
			logger.verbose("Register %s for %s" % (cls, tokenClass))
			if cls.styles:
				AbstractNode.styles |= cls.styles
				cls.styles = AbstractNode.styles
			if tokenClass not in cls.classByToken: 
				AbstractNode.classByToken[tokenClass] = [cls]
			else: 
				AbstractNode.classByToken[tokenClass].append(cls)

	@classmethod
	@staticmethod
	def createFromToken(token,parent):
		tokenType = type(token)
		good_class = AbstractNode.classByToken['none'][0]
		if not tokenType in AbstractNode.classByToken:
			logger.warning("Ignore %s because it's not implemented." % tokenType)
		else:
			for c in AbstractNode.classByToken[tokenType]:
				if c.condition(token,parent):
					good_class = c
				else:
					logger.spam("%s condition isn't good." % c)
			logger.debug("Generate %s for %s with parent %s" % (good_class,tokenType,parent))

		return good_class(token,parent)

	@staticmethod
	def condition(block,parent):
		return True
	
	def __init__(self, block=None, parent=None, children=[]):
		super().__init__()
		self._id = ""
		self._block = block
		self.parent = parent
		self.children = children

	def __str__(self):
		return "<%s,id=%s>" % (self.__class__.__name__,self.id)

	def _checkStyles(self):
		for k,s in self.styles.items():
			for st in self.files.tplDocx.styles:
				if st.style_id == s:
					AbstractNode.tplStyles[k] = st
					break
			else:
				logger.warning("Can't found '%s' style inside template." % s)

	def getStyleById(self, id=None):
		if not id:
			id = self.id
		return self.files.getTplByKey(id)[1]

	def getPById(self, id=None):
		if not id:
			id = self.id
		return self.files.getTplByKey(id)[0]

	@property   
	def id(self):
		if not self.parent:
			return ""
		else:
			pid = self.parent.id
			if self._id:
				if pid:
					return "%s.%s" % (pid,self._id)
				else:
					return self._id
			else:
				return pid

	@property
	def files(self):
		return AbstractNode._files

	@files.setter
	def files(self,files):
		needCheckStyle = not hasattr(AbstractNode,'_files')
		AbstractNode._files = files
		if needCheckStyle:
			self._checkStyles()
		

	def generate(self):
		logger.warning("%s must implement generate method" % self.__class__)
		return {}
