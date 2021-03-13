import uuid

from nodes import AbstractNode, TextNode

from docxtpl import RichText
from mistletoe.block_token import Table


class TableNode(AbstractNode, tokenClass=Table):
	# Table xml format. It's perfect for a second rendering BY python docx template BUT NOT BY WORD !
	rawxml = '''<w:p><w:r><w:t xml:space="preserve"><w:tbl><w:tblPr><w:tblStyle w:val="mddottable"/><w:tblW w:w="0" w:type="auto"/><w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr><w:tblGrid><w:gridCol w:w="2439"/><w:gridCol w:w="2207"/><w:gridCol w:w="2208"/></w:tblGrid><w:tr>{%% for col in %s %%}<w:tc><w:tcPr><w:tcW w:w="2207" w:type="dxa"/></w:tcPr><w:p><w:pPr><w:rPr></w:rPr></w:pPr><w:r><w:rPr></w:rPr><w:t xml:space="preserve"></w:t></w:r>{{ col }}<w:r><w:t xml:space="preserve"></w:t></w:r></w:p></w:tc>{%% endfor %%}</w:tr>{%% for row in %s %%}<w:tr>{%% for col in row %%}<w:tc><w:tcPr><w:tcW w:w="2207" w:type="dxa"/></w:tcPr><w:p><w:pPr><w:rPr></w:rPr></w:pPr><w:r><w:rPr></w:rPr><w:t xml:space="preserve"></w:t></w:r>{{ col }}<w:r><w:t xml:space="preserve"></w:t></w:r></w:p></w:tc>{%% endfor %%}</w:tr>{%% endfor %%}</w:tbl></w:t></w:r></w:p>'''

	def __init__(self, block, parent=None, children=[]):
		super().__init__(block, parent, children)
		# TODO implement alignment compatibility
		# None -> Left, 0 -> center, 1 -> right
		self.column_align = block.column_align

		self.headers = []
		for header in block.header.children:
			data_header = []
			for e in header.children:
				e = TextNode(e)
				data_header.append(e)
			self.headers.append(data_header)

		self.data = []
		for row in block.children: 
			# TableRow
			data_row = []
			for col in row.children: 
				# TableCol
				data_col = []
				for e in col.children:
					data_col.append(TextNode(e))
				data_row.append(data_col)
			self.data.append(data_row)

	def generate(self,rt_parent = None):
		context = {
			'headers':[],
			'data':[],
		}

		if self.headers:
			for header in self.headers:
				rt = RichText()
				for e in header:
					rt.xml += e.generate().xml
				context['headers'].append(rt)

		for row in self.data:
			context_row = []
			for col in row:
				rt = RichText()
				for e in col:
					rt.xml += e.generate().xml
				context_row.append(rt)
			context['data'].append(context_row)


		idTable = 'table_'+str(len(self.tables))
		xml = self.rawxml % (idTable+".headers",idTable+".data")
		context['xml'] = xml
		self.tables[idTable] = {'headers':context['headers'],'data':context['data']}
		
		return context