from compiler import Compiler
from interpreter import Interpreter 

# Import smtplib for the actual sending function
import smtplib
import time
from email.mime.text import MIMEText
from email.utils import formatdate
from email.mime.text import MIMEText

import flask
app = flask.Flask(__name__)
DEBUG=True
code=""
#IMPORTANT: Need to configure these for message sending to work
SENDER='' #Gmail address to send messages
PASSWORD='' #SENDER password
TARGET=''#Where to send the messages

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/',methods=['GET', 'POST'])
def main():
	global code
	if code=="":
		hasCode=False;
	else:
		hasCode=True
	if flask.request.method == 'POST':
		print('it is posting')
		if flask.request.form['submit']=='convert':
			if flask.request.form['code']!="":
				code=Compiler.runCompiler(flask.request.form['code'])
			else:code=""
		elif flask.request.form['submit']=='textMe':
			sendMessage(message_text=code)
			code=""
		return flask.redirect('/redirect')
	context={'code':code,'hasCode':hasCode}
	return flask.render_template('mainpage.html', **context)
	
	
@app.route('/redirect')
def redirect():	
	return flask.redirect('/')
	
	
def sendMessage(message_text='No Message Content',target=TARGET):
	print(message_text)
	message = MIMEText(message_text)
	message['Date'] = formatdate()
	message['From'] = SENDER
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(SENDER, PASSWORD)
	server.sendmail(SENDER, TARGET, message.as_string())
	server.quit()
"""
myMessage=str(Compiler.runCompiler("Say Hello 6 times"))
print(myMessage)
sendMessage(myMessage)
"""
if __name__ == '__main__':
	app.run(debug=DEBUG) 
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
