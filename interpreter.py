import string
import math
def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0
	
    return result + current
class Interpreter():

	keywords={}
	myVariables={}
	
	@classmethod
	def addKeywords(cls,words,function_name):
		#words is a list of keyword strings
		#function_name is a string
		for word in words:
			if (word in cls.keywords):
				workingList=cls.keywords[word]
				workingList.append(function_name)
				cls.keywords[word]=workingList
			else:
				cls.keywords[word]=[function_name]
	def splitIntoSentences(stringIn):
		sentences=stringIn.split('.')
		return [sentence for sentence in sentences if sentence != ""]
		
	def stripPunctuation(stringIn):
		stringOut=stringIn
		for char in stringIn:
			if char in string.punctuation:
				stringOut=stringOut[1:]
			else:
				break
		reverse=""
		for char in stringOut:#constructing reversed string
			reverse=char+reverse
		for char in reverse:
			if char in string.punctuation:
				reverse=reverse[1:]
			else:
				break
		stringOut=""
		for char in reverse:#constructing reversed string
			stringOut=char+stringOut
		#Also do alphanumneric lowering
		stringOut=stringOut.lower()
		return stringOut
	
	@classmethod
	def makeWordsList(cls,stringIn):
		stringIn=cls.stripPunctuation(stringIn)
		words=[]
		for word in stringIn.split():
			if word != None:
				words.append(word)
		return words
	
	def removeKeywordInstance(stringIn,my_keyword):
		unpackedValues=[]
		values = Interpreter.getValues(stringIn)
		for value in values:
			try:
				for key_value in Interpreter.keywords[value['value']]:
					if key_value==my_keyword:
						#print('appending ^')
						pass
					else:unpackedValues.append(value)
				#print (Interpreter.keywords[value['value']])
			except:unpackedValues.append(value)
		#return unpackedValues
		stringOut=""
		for word in unpackedValues:
			stringOut+=str(word['value'])
			stringOut+=" "
		return stringOut
	def removeFirstKeywordInstance(stringIn,my_keyword):
		unpackedValues=[]
		isFirst=True
		values = Interpreter.getValues(stringIn)
		for value in values:
			try:
				for key_value in Interpreter.keywords[value['value']]:
					if key_value==my_keyword:
						if isFirst:
							isFirst=False
					else:unpackedValues.append(value)
				#print (Interpreter.keywords[value['value']])
			except:unpackedValues.append(value)
		#return unpackedValues
		stringOut=""
		for word in unpackedValues:
			stringOut+=str(word['value'])
			stringOut+=" "
		return stringOut		
	@classmethod
	#takes a string
	#returns a list of function dictionaries for the string, with corresponding indexes and a list of possible functions.
	def getFunctions(cls,stringIn,distinct=True):
		functions=[]
		index=0
		words=cls.makeWordsList(stringIn)
		for word in words:
			if (word in cls.keywords):
				functions.append({'index':index, 'functions':cls.keywords[word]})
			index+=1
		#distinct functionality not implemented
		return functions
	
	
	@classmethod
	def getAssociatedNumbers(cls,stringIn):
		numbers=[]
		stringIn=cls.stripPunctuation(stringIn)
		for number in stringIn.split():
			try:
				numbers.append(float(number))
			except:pass
		return numbers
	@classmethod
	def getValuesOfType(cls,stringIn,type):
		output=[]
		values=cls.getValues(stringIn)
		for value in values:
			if value['type']==type:
				output.append(value)
		return output
	@classmethod
	def getValues(cls,stringIn):
		values=[]
		stringIn=cls.stripPunctuation(stringIn)
		index=0
		for value in stringIn.split():
			try:
				number = float(value)
				if number.is_integer():
					values.append({'type':'int','index':index,'value':int(number)})
				else:
					values.append({'type':'float','index':index,'value':float(number)})
			except:
				try:
					values.append({'type':'int','index':index,'value':text2int(value)})
				except:
					values.append({'type':'str','index':index,'value':value})
			index+=1
		return values
	
	@classmethod		
	def hasNumbers(cls,stringIn):
		if len(cls.getAssociatedNumbers(stringIn))>0:
			return True
		else:
			return False
	
	@classmethod
	def getDefiniteFunctions(cls,stringIn):
		definiteFunctions=[]
		functions=cls.getFunctions(stringIn)
		for function in functions:
			if len(function['functions'])==1:
				definiteFunctions.append(function['functions'][0])
		return list(set(definiteFunctions))
	@classmethod
	def getPossibleFunctions(cls,stringIn):
		#need to check if this works
		possibleFunctions=[]
		functions=cls.getFunctions(stringIn)
		for function_group in functions:
			for function in function_group['functions']:
				possibleFunctions.append(function)
		return list(set(possibleFunctions))	
	@classmethod
	def runInterpreter(cls,stringIn):
		definiteFunctions=cls.getDefiniteFunctions(stringIn)
		possibleFunctions=cls.getPossibleFunctions(stringIn)
		if set(definiteFunctions)==set(possibleFunctions):#is aliasing an issue?
			#Definite cases
			if len(definiteFunctions)==1:
				return cls.runFunction(definiteFunctions[0],stringIn)
			elif 'loop' in definiteFunctions:
				return cls.runFunction('loop',stringIn)
			elif 'assignment' in possibleFunctions:
				return cls.runFunction('assignment',stringIn)
			elif 'print' in definiteFunctions:
				return cls.runFunction('print',stringIn)
		else:#Handling for blurry cases
			pass #passing for now- will implement later.
		
		
	@classmethod
	def runFunction(cls,function,stringIn): 
	#function should be passed in a string.
		if function == 'loop':
			return cls.Functions.evaluateLoop(stringIn)
		if function == 'print':
			return cls.Functions.evaluatePrint(stringIn)
		
	def getInput(prompt):
	#prompt the user for input
	#prompt is passed in as a string
		return input("{}: ".format(prompt))
	"""
	@classmethod
	def splitByConjunctions(cls,stringIn):
		for conjunction in cls.keywords['conjunctions']:
	"""	
			
	class Functions():
		@classmethod
		def evaluatePrint(cls,stringIn):
			subString=Interpreter.removeFirstKeywordInstance(stringIn,'print')
			
			if cls.hasMath(stringIn):
				
				functionOut={'function':'print','args':{},'children':[]}
				#ADD STUFF HERE
			else:
				return {'function':'print','args':{'string':subString},'children':[]}
			
		@classmethod
		def evaluateLoop(cls,stringIn):
			if len(Interpreter.getValuesOfType(stringIn,'int'))>0:
				#possible 
				if len(Interpreter.getValuesOfType(stringIn,'int'))==1:#Only one loop quantity argument
					loopCount=Interpreter.getValuesOfType(stringIn,'int')[0]['value']
					#assuming that we are just passed subloop info
					functionOut = {'function':'loop','args':{'loopCount':loopCount},'children':[]}
					subString=cls.unpackFromLoop(stringIn)
				else:#multiple value arguments
					closestIndex=None
					smallestDistance=None
					keyWordIndex=20#favor the end of sentence?
					loopCount=None
					for word in Interpreter.getValues(stringIn):
						if word['value'] in Interpreter.keywords:
							if Interpreter.keywords[word['value']]=='loop':
								keyWordIndex=word['index']
								break
					for word in Interpreter.getValuesOfType(stringIn,'int'):
						if closestIndex==None or abs(keyWordIndex-word['index'])<smallestDistance:
							closestIndex=word['index']
							loopCount=word['value']
							smallestDistance=abs(keyWordIndex-closestIndex)
					functionOut = {'function':'loop','args':{'loopCount':loopCount},'children':[]}	
							
								
					#implement later
					
					subString=cls.unpackFromLoop2(stringIn,closestIndex)
				children=cls.copyOverFunction(subString)
				for child in children:
					functionOut['children'].append(Interpreter.runInterpreter(child))
			return functionOut
		def hasMath(stringIn):
			subString=stringIn
			subString=Interpreter.removeKeywordInstance(subString,'plus')
			subString=Interpreter.removeKeywordInstance(subString,'subtract')
			subString=Interpreter.removeKeywordInstance(subString,'divide')
			subString=Interpreter.removeKeywordInstance(subString,'multiply')
			subString=Interpreter.removeKeywordInstance(subString,'modulo')
			if set(Interpreter.makeWordsList(subString))==set(Interpreter.makeWordsList(stringIn)):
				return False
			else:
				return True
		def unpackFromLoop(stringIn):
			#assumes that loop is parent
			#removes all value arguments
			unpackedValues=[]
			values = Interpreter.getValues(stringIn)
			for value in values:
				#print(value)
				#print(Interpreter.keywords['print'])
				if value['type']!='int':#Not an int value:
					#print (Interpreter.keywords[value['value']])
					try:
						if Interpreter.keywords[value['value']][0]=='loop':
							pass
						else:unpackedValues.append(value)
							
					except:unpackedValues.append(value)
			#return unpackedValues
			
			stringOut=""
			for word in unpackedValues:
				stringOut+=word['value']
				stringOut+=" "
			return stringOut	#return as string
			
		def unpackFromLoop2(stringIn,loopCountIndex):
			#assumes that loop is parent
			#removes all value arguments
			unpackedValues=[]
			values = Interpreter.getValues(stringIn)
			for value in values:
				#print(value)
				#print(Interpreter.keywords['print'])
				if value['index']!=loopCountIndex:#Not the loop count index
					#print (Interpreter.keywords[value['value']])
					try:
						if Interpreter.keywords[value['value']][0]=='loop':
							pass
						else:unpackedValues.append(value)
							
					except:unpackedValues.append(value)
			#return unpackedValues
			
			stringOut=""
			for word in unpackedValues:
				stringOut+=str(word['value'])
				stringOut+=" "
			return stringOut	#return as string
			
		def splitByNext(stringIn):
			unpackedValues=[]
			values = Interpreter.getValues(stringIn)
			for value in values:
				try:
					if Interpreter.keywords[value['value']][0]=='next':
						#print('appending ^')
						unpackedValues.append({'value':'^'})
					else:unpackedValues.append(value)
					#print (Interpreter.keywords[value['value']])
				except:unpackedValues.append(value)
			#return unpackedValues
			stringOut=""
			for word in unpackedValues:
				stringOut+=str(word['value'])
				stringOut+=" "
				
			return stringOut.split('^')
		
		@classmethod
		def copyOverFunction(cls,stringIn):
			strings=cls.splitByNext(stringIn)
		
			#print (strings)
			functionsToCopy=None
			functions=[]
			stringsOut=[]
			for	string in strings:
				if Interpreter.getPossibleFunctions(string)==[] and len(functions)!=0:
					#print('Tabah!')
					#this string doesn't have functions, and the preceding one does
					#COPY OVER OLD FUNCTIONS
					for function in functions:
					#	print ("BA:{}".format(function))
						workingString=""
						workingString+=(function)
						workingString+=" "
						string=workingString+string
				else:
					#print("SLAH:{}".format(Interpreter.getPossibleFunctions(string)))
					functions=[]
					for word in Interpreter.makeWordsList(string):
					#	print (word)
						if word in Interpreter.keywords:
							functions.append(word)
					#print ('functions: {}'.format(functions))
				stringsOut.append(string)
			return stringsOut
					
		
			
			

def initialize():
	#Loops
	loop=['times','loop']
	Interpreter.addKeywords(words=loop,function_name='loop')
	
	#MATH
	add=['add','plus']#add
	Interpreter.addKeywords(words=add,function_name='add')
	subtract=['minus','subtract']#subtract
	Interpreter.addKeywords(words=subtract,function_name='subtract')
	multiply=['multiply']#times
	Interpreter.addKeywords(words=multiply,function_name='multiply')
	divide=['divide','over','division']#divide
	Interpreter.addKeywords(words=divide,function_name='divide')
	modulo=['modulo','remainder','remaining']#modulo
	Interpreter.addKeywords(words=multiply,function_name='multiply')
	
	#LOGIC
	#equals=['equals','equal', 'is','be','same']#equals OR assignment
	#Interpreter.addKeywords(words=equals,function_name='equals')
	negators=['not',"isn't","don't"]#equals OR assignment
	Interpreter.addKeywords(words=negators,function_name='not')
	ifs=['if']#equals OR assignment
	Interpreter.addKeywords(words=ifs,function_name='if')
	
	#VARIABLE HANDLING
	assignment=['equals','equal', 'is','be','same']#,'store','let','set']
	Interpreter.addKeywords(words=assignment,function_name='assignment')
	name=['called','define', 'named']#nameDeclaration
	Interpreter.addKeywords(words=name,function_name='nameDeclaration')
	
	#GENERAL OUTPUTS
	prints=['print','display','say','show','write']
	Interpreter.addKeywords(words=prints,function_name='print')
	
	#SEPERATORS
	conjunctions=['and']
	Interpreter.addKeywords(words=conjunctions,function_name='conjunctions')
	nextBreak=['then','next','finally','than']
	Interpreter.addKeywords(words=nextBreak,function_name='next')

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\TESTS////////////////////////////////////////////////////

if __name__ == '__main__':
	initialize()
	#loops=['times','loop','keep']
	#Interpreter.addKeywords(words=loops,function_name='loop')
	print (Interpreter.getFunctions("This is our   string coming in 5 times times."))
	print (Interpreter.hasNumbers("This is number 52, and now 3"))
	print (Interpreter.hasNumbers("This is a string with no numbers"))
	print (Interpreter.getDefiniteFunctions("This is our   string coming in 5 times times."))
	print(Interpreter.getValues("We have numbers 3 and 4 and 5"))
	print(Interpreter.getInput("Type a number"))
	Interpreter.runInterpreter("loop 23 times")
	print(Interpreter.stripPunctuation("..'sloop',"))
	print(Interpreter.splitIntoSentences('I like you.you like me... let me oh no wait.'))
	Interpreter.runInterpreter("Print the dog's name then print the cat's name 5 times")
	print(Interpreter.Functions.unpackFromLoop("Do something 5 times loop"))
	print(Interpreter.Functions.splitByNext("print this then that"))
	print(Interpreter.Functions.copyOverFunction("print this then that"))
	print(Interpreter.runInterpreter('print this then that 10 times'))
	#Say hello twelve times
	#Add two plus two
	#find the answer to ...
