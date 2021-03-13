from mistletoe import Document, markdown
from mistletoe.ast_renderer import ASTRenderer
from docxtpl import DocxTemplate

from nodes import TextNode
from logger import logger
from md_parser import Parser

import os

class Project:
	TMP_FILENAME = "temp.docx"

	def __init__(self,mdFilename,templateFilename,output):
		logger.verbose("Project initialization : %s, %s, %s" % (mdFilename, templateFilename, output))
		
		self._mdFilename = mdFilename
		
		with open(mdFilename,'r') as f:
			self._rawMd = f.read()

		self.md = Document(self._rawMd)
		self._templateFilename = templateFilename
		self.template = DocxTemplate(templateFilename)

		self.parsedTree = Parser(self.md,self.template,mdFilename)
		logger.debug("Parsed Tree:\n" + str(self.parsedTree))

		context = self.parsedTree.generateDocx()
		logger.spam("context: %s" % context)

		logger.info('First rendering start.')
		self.template.render(context)
		self.template.save(output+self.TMP_FILENAME)
		
		logger.info('Second rendering start.')
		self.template = DocxTemplate(output+self.TMP_FILENAME)
		self.parsedTree.finalize(self.template)
		self.template.render(context)
		self.template.save(output)
		logger.info('Full rendering finished.')

		os.remove(output+self.TMP_FILENAME) 

		# self.output = output
		# self.template.save(output)
