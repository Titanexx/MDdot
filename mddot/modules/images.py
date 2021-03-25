import helpers
from modules import AbstractModule
from logger import logger

from docx.shared import Length
from docxtpl import InlineImage
from PIL import Image

import time

class Images(AbstractModule):
	def runFirst(self,context):
		for id,img in context['images'].items():
			p = self.files.getTplByKey(img['id'])[0]
			if p:
				im = Image.open(img['src'])

				if "_Body" in str(type(p._parent)):
					section = p._parent._element.xpath(".//following::w:sectPr")[0]
					length=section.page_width - (section.right_margin + section.left_margin) 
				else:			
					rightMargin = helpers.getMarginFromStyle(p._parent._parent.style,'right')
					leftMargin = helpers.getMarginFromStyle(p._parent._parent.style,'left')
					length = Length(p._parent.width) - (rightMargin + leftMargin)

				width, height = im.size
				dpiWidth, dpiHeight = im.info['dpi']
				widthEmus = width / dpiWidth * Length._EMUS_PER_INCH
				heightEmus = height / dpiHeight * Length._EMUS_PER_INCH
				imgWidth = widthEmus
				if widthEmus > length:
					imgWidth = length

				logger.debug("Load image %s inside %s." % (img,self.files.tplFilename))
				img['img'] = InlineImage(self.files.tpl,img['src'],imgWidth)
			else:
				logger.warning("Inserting image %s failed. Key is not found." % img['id'])