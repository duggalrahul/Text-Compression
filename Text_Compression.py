__author__ = "Rahul Duggal"
__email__ = "rahulduggal2608[at]gmail[dot]com"


from operator import itemgetter
import re


class compress:
	'''
	# syntax : c = compress(fileName, dictionarySize)
	#          so if we have c = compress('text.txt',100), then
	#          we are compressing the file named text.txt and we replace 100 words
	#          The compressed file can be accesed as c.compressedFile
	'''

	def __init__(self, readFileName, num):
		self.readFileName = readFileName

		# self.num is the number of element in the key
		self.num = num	

		# self.lines stores the file as a list of lines of the file
		self.lines = []

		# self.d stores the frequency of occurence of each word.
		self.d = {}

		# self.l stores the list of tuples as explained later.
		self.l = []	

		# self.key stores the best words to replace. it maps words to their coded text	
		self.key = {}

		#self.compressedFile stores the coded file as a list of strings. 
		self.compressedFile = []

	def compressFile(self):
		self.readFile()
		self.buildDict()
		self.optimise()
		self.buildList()
		self.sortedList()
		self.buildKey()
		self.searchAndReplace()

	def readFile(self):
		f = open(self.readFileName,'r')
		self.lines = f.readlines()
		f.close()
	
	# this method builds the dictionary self.d calculating frequency of each word.
	# since the replacements are from ~0 to ~99, we replace only those elements
	# with length > 3 and that are not whitespace
	def buildDict(self):
		for line in self.lines:

			# we split each line on whitespace characters using .split() method.
			for word in line.split():	
			    # add each element with length>3 to self.d and update frequency			
				if len(word)>3:
					if word in self.d.keys():
						self.d[word] = self.d[word]+1
					else:
						self.d[word] = 1

	# this calculates freq * length for every word in passage.
	# so if '^' occurs 15 times and 'hello' occurs 4 times
	# self.d['^'] = 1*15 and self.d['hello'] = 4*5
	# so 'hello' gets a higher rank than '^' even though '^' occurs more frequently
	def optimise(self):
		for k in self.d.keys():
			self.d[k] = self.d[k] * len(k)
    
    # by now we have freq * len of all words in our file. We need to find the best words
    # to replace. Since sorting is not supported in dictionary, we need to build a list
    # and sort on the basis of freq * length

    # this method builds a list of tuples self.l where
    # each element in the list is a (word , freq * length) tuple
	def buildList(self):
		for word in self.d.keys():
			# t is a tuple with first element as the word
			# and the second element as its freq * len.
			t = (word,self.d[word])	
			self.l.append(t)

	# this method sorts the list of tuples according to freq * length
	# i.e. the second element of the tuple.
	def sortedList(self):
		self.l = sorted(self.l, key=itemgetter(1), reverse=True)

	# this method builds a dictionary 'self.num', of the best words with their replacements
	# so the best word maps to ~0, second best to ~1 and so on..
	# for example self.key['hackathon'] = '~10'. if 'hackathon' has rank 10 in the sorted list.
	def buildKey(self):
		for i in range(self.num):
			self.key[self.l[i][0]] = ('~'+str(i), self.l[i][1])

	# this method looks up each word in the dictionary
	# if found, it replaces with ~rank
	# so if "hello" gets the highest weight, it gets mapped to ~0
	def searchAndReplace(self):
		for line in self.lines:
			# list 'line' converts to list 'newLine' after replacing with the code text.
			newLine = []
			# here I split each line into a list of strings according to whitespace, using
			# the regular expression (\s+) with the re.split() method.
			# using re.plit() instead of .split() here is important since we need to preserve the delimiters
			# such as spaces, tabs, etc to retain formatting.
			# so for example re.split(r'(\s+)','It is a beautiful day 	') would return
			# ['It', ' ', 'is', ' ', 'a', ' ', 'beautiful', ' ', 'day', ' \t', '']
			# original text can be reassembled from the above list by using the "".join() method
			for word in re.split(r'(\s+)',line):
				# if word is found in key, replace it
				if word in self.key.keys():
					newLine.append(self.key[word][0])
				# if not found in key, use original word
				else:
					newLine.append(word)
			
			self.compressedFile.append("".join(newLine))	

	# this method prints in the following in order
	# dictionary size
	# dictionary 
	# compressed text
	def printFile(self, writefileName):
		f = open(writefileName,'w')
		f.write(str(self.num)+'\n')
		for word in self.key.keys():
			f.write(word + ' ' + self.key[word][0] + '\n')
		for line in self.compressedFile:
			f.write(line)
		f.close()


class decompress:
	'''
	# syntax : decompress(fileName)
	#          so if we have d = decompress('text.txt'), then
	#          we are decompressing the file named text.txt
	#          The decompressed file can be accesed as c.originalFile
	'''

	def __init__(self, readFileName):
		self.readFileName = readFileName
		# self.num stores the number of elements in the key. ie number of coded words
		self.num = 0
		# self,lines stores the text file as a list of strings of each line.
		self.lines = []
		# self.revkey maps the coded text to the original word.
		self.revKey = {}
		#self.originalFile stores the decoded file as a list of strings of each line.
		self.originalFile = []

	def decompressFile(self):
		self.readFile()
		self.buildReverseKey()
		self.searchAndReplace()

	# this function reads the compressed file.
	# the first line of the compressed file should contain
	# the dictionary size
	def readFile(self):
		f = open(self.readFileName,'r')
		self.lines = f.readlines()
		# self.num is the number of elements in the key. 
		# first line of the coded text stores this value
		self.num = int(self.lines[0].split()[0])
		f.close()

	#this method builds the key using the lines 1 to self.num, of the compressed file
	# so if 'hello' mapped to ~5 in the original key while encoding, now
	# ~5 maps to 'hello' while decoding.
	def buildReverseKey(self):
		for line in self.lines[1:self.num+1]:
			l = line.split()
			self.revKey[l[1]] = l[0]

	# this method replaces the code words with their original word
	# again using the regular expression is important here to preserve the formatting
	def searchAndReplace(self):
		for line in self.lines[self.num+1:]:
			newLine = []
			for word in re.split(r'(\s+)', line):
				if word in self.revKey.keys():
					newLine.append(self.revKey[word])
				else:
					newLine.append(word)
			self.originalFile.append("".join(newLine))

	def printFile(self, writeFileName):
		f = open(writeFileName,'w')
		for line in self.originalFile:
			f.write(line)
		f.close()

def main():
	
	# start compression	
	c = compress('text.txt', 100)	
	c.compressFile()
	c.printFile('compressed.txt')	

	
	# start decompression	
	d = decompress('compressed.txt')	
	d.decompressFile()
	d.printFile('originalFile2.txt')
	
if __name__ == '__main__':
	main()