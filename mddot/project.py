from docxtpl import DocxTemplate

from modules import AbstractModule
from logger import logger
from md_parser import Parser
from files import Files

import os
import json

class Project:
	def __init__(self,mdFilename,tplFilename,outFilename):
		self.files = Files(mdFilename,tplFilename,outFilename)

		logger.info('Call modules before parsing')
		for module in AbstractModule.MODULES:
			module(self.files).runBeforeParsing()

		self.parsedTree = Parser(self.files)
		logger.debug("Parsed Tree:\n" + str(self.parsedTree))

		context = self.parsedTree.generateDocx()
		logger.spam("context: %s" % json.dumps(context,default=str))
		logger.info('Call modules before rendering')
		for module in AbstractModule.MODULES:
			module(self.files).runBeforeRendering(context)

		logger.info('Rendering start')
		self.files.tpl.render(context)
		self.files.tpl.save(outFilename)
		self.files.tplFilename = outFilename
		
		logger.info('Call modules after rendering')
		for module in AbstractModule.MODULES:
			module(self.files).runAfterRendering(context)

		logger.info('Rendering finished.')
