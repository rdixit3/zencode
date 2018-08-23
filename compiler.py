from interpreter import Interpreter 
from interpreter import initialize


class Compiler():
	def setSaveTarget():
		pass
	@classmethod
	def writeNormalLoop(cls,iterations,childFunctions,iterator_name='n'):
		outputString="for {} in range(0,{}):\n".format(iterator_name,iterations)
		if len(childFunctions)==0:
			outputString+='	pass\n'
		else:
			for child in childFunctions:
				outputString+="	{}".format(cls.doFunction(child))
			pass
		return outputString
	def writePrintString(string):
		return "print('{}')\n".format(string.strip())
	@classmethod		
	def doFunction(cls,function):#redirect to respective function writers
		if function['function']=='loop':
			if 'loopCount' in function['args']:
				#print (function['args']['loopCount'])
				return cls.writeNormalLoop(iterations=function['args']['loopCount'],childFunctions=function['children'])
		#print ('print passed')
		#print(function)
		if function['function']=='print':
			#print('strobo')
			#print(function['args']['string'])
			return cls.writePrintString(function['args']['string'])
	
	@classmethod	
	def runCompiler(cls, stringIn):
		"""
		function=Interpreter.runInterpreter(stringIn)
		return cls.doFunction(function)
		"""
		try:
			strings=Interpreter.splitIntoSentences(stringIn)
			outputCode=""
			for string in strings:
				print (string)
				function=Interpreter.runInterpreter(string)
				outputCode+= cls.doFunction(function)
				
			return outputCode
		except:return "Sorry, could not compile"
		
		
#print (Compiler.writeNormalLoop(12,[]))
initialize()
if __name__ == '__main__':
	
	myFunction={'function':'loop','args':{'loopCount':12},'children':[]}
	print (Compiler.doFunction(myFunction))
	print(Compiler.runCompiler("print this then that 5 times"))
	print(Compiler.runCompiler("for 5 times, print bitcamp"))
	print(Compiler.runCompiler("say hello five times"))
#determining models {'function':'loop','args':{loopCount:12},'children':[{},{}]}

