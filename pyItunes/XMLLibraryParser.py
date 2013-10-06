#
# This is file is DEPRECIATED, however, updated here to allow compatability with older code using pyItunes
#
import plistlib

class XMLLibraryParser:
	def __init__(self,xmlLibrary):
		#Much better support of xml special characters
		self.dictionary = plistlib.readPlist(xmlLibrary)['Tracks']
		
