from docxtpl import DocxTemplate

from modules import AbstractModule
# from nodes import TextNode
from logger import logger
from md_parser import Parser
from files import Files

import os
import json

from jinja2 import Undefined, Environment

class SilentUndefined(Undefined):
	def _fail_with_undefined_error(self, *args, **kwargs):
		return ''


class Project:
	TMP_FILENAME = "temp.docx"

	def __init__(self,mdFilename,tplFilename,outFilename):
		self.files = Files(mdFilename,tplFilename,outFilename)
		jinjaEnv = Environment(undefined=SilentUndefined)

		self.parsedTree = Parser(self.files)
		logger.debug("Parsed Tree:\n" + str(self.parsedTree))

		context = self.parsedTree.generateDocx()
		logger.spam("context: %s" % json.dumps(context,default=str))

		logger.info('First rendering start.')
		self.files.tpl.render(context,jinja_env=jinjaEnv)
		self.files.tpl.save(self.TMP_FILENAME)
		self.files.tplFilename = self.TMP_FILENAME
		
		logger.info('Modules calling.')
		for module in AbstractModule.MODULES:
			module(self.files).runFirst(context)

		logger.info('Second rendering start.')
		self.files.tpl.render(context,jinja_env=jinjaEnv)
		self.files.tpl.save(outFilename)
		self.files.tplFilename = outFilename

		logger.info('Modules calling.')
		for module in AbstractModule.MODULES:
			module(self.files).runSecond(context)

		logger.info('Full rendering finished.')

		os.remove(self.TMP_FILENAME) 
