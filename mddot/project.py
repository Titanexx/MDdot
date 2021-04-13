from .files import Files
from .logger import logger
from .modules import AbstractModule
from .md_parser import Parser

import json
import os

from docxtpl import DocxTemplate

class Project:
	def __init__(self,mdFilename,tplFilename,outFilename):
		self.files = Files(mdFilename,tplFilename,outFilename)

		logger.info('Calling modules before parsing')
		for module in AbstractModule.MODULES:
			module(self.files).runBeforeParsing()

		self.parsedTree = Parser(self.files)
		logger.debug("Parsed Tree:\n" + str(self.parsedTree))

		context = self.parsedTree.generateDocx()
		logger.spam("context: %s" % json.dumps(context,default=str))
		logger.info('Calling modules before rendering')
		for module in AbstractModule.MODULES:
			module(self.files).runBeforeRendering(context)

		logger.info('Start of rendering')
		self.files.tpl.render(context)
		self.files.tpl.save(outFilename)
		self.files.tplFilename = outFilename
		logger.info('End of rendering')
		
		logger.info('Calling modules after rendering')
		for module in AbstractModule.MODULES:
			module(self.files).runAfterRendering(context)

		logger.info('Your document is generated. Enjoy !')


