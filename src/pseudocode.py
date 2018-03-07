class PCProgram:
	def __init__(self):
		pass

class PCInstruction:
	ARG_VARNAME = 0
	ARG_TEXT	= 1
	ARG_NUMBER	= 2
	ARG_EXPR	= 3
	ARG_BOOL	= 4

	def __init__(self):
		pass

	def exec(self, arguments, children):
		pass

	def can_haz_children():
		return False

	def get_arguments():
		return []

	def __str__(self):
		return "this shouldn't ever happen, ever"

class PCI_Input(PCInstruction):
	def get_arguments():
		return [ARG_VARNAME]