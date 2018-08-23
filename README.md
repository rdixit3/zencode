# zencode
Generate python code from pseudo-code

To use, just download all of the files, and run alexa.py. Needs python 3 and Flask installed.

Developed at Bitcamp 2017 - Matthew Fan and Rohan Dixit

----------------------------------------------------------
Q:	What is Zencode?
A:	Zencode is a flexible programming language without a formal syntax which interprets psuedo-code-like, 
	natural language into compilable python code (hopefully more languages coming soon).

Q:	How does Zencode work?
A:	Simply type what you want Zencode to do. It identifies words that are designated as possible function words,
	and extracts those into a list where it analyzes possible code blocks that can be comprised of the given functions
	and arguments. In the case that there is ambiguity, Zencode can prompt the user for clarification.