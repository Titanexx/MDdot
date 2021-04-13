from ..helpers import MDict
from ..nodes import AbstractNode

class RootNode(AbstractNode):
	def __init__(self, files, **args):
		super().__init__(*args)
		self.files = files

	def generate(self):
		context = MDict()

		for child in self.children:
			childContext = child.generate()
			if "_full_xml" in childContext:
				context["_full_xml"] += childContext["_full_xml"]
				del(childContext["_full_xml"])
			context = context | childContext

		print(context["_full_xml"])

		return context

	def generate(self):
		context = MDict({"_full_xml": ""})

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
					if "_full_xml" in v:
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
					if "_full_xml" in v:
						context["_full_xml"] += v["_full_xml"]

		return context