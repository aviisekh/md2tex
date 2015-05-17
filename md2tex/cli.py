#!/usr/bin/python

#md2TeX

import sys,os,re,subprocess
from data import *

doc_class = sys.argv[3].lower()

table_active = False
table_head_active = False
list_active = []
list_active.append(False)
list_tab = 0
linenumber = 0
column = 0
program_error = False

#fixed
def error_message(msg,line_no):

	global program_error	
	print '\033[1m'
	if(line_no==None):
		print msg
	else:
		print 'In line '+str(line_no)+' : '+msg
	print' \033[0m'
	program_error = True
	

#fixed
def structure(sentence):

	if sentence[1]!='#':
		if doc_class=='letter':
			error_message('Parts not allowed in letters',linenumber)
		else:
			tex_body.write('\part{'+sentence[1:][:-1]+'}\n')
	elif sentence[2]!='#':
		if doc_class!='report' and doc_class!='book':
			error_message('Chapters allowed only in reports and books',linenumber)
		else:
			tex_body.write('\chapter{'+sentence[2:][:-1]+'}\n')
	elif sentence[3]!='#':
		if doc_class=='letter':
			error_message('Sections not allowed in letters',linenumber)
		else:
			tex_body.write('\section{'+sentence[3:][:-1]+'}\n')
	elif sentence[4]!='#':
		if doc_class=='letter':
			error_message('Subsections not allowed in letters',linenumber)
		else:
			tex_body.write('\subsection{'+sentence[4:][:-1]+'}\n')
	elif sentence[5]!='#':
		if doc_class=='letter':
			error_message('Subsubsections not allowed in letters',linenumber)
		else:
			tex_body.write('\subsubsection{'+sentence[5:][:-1]+'}\n')
	elif sentence[6]!='#':
		if doc_class=='letter':
			error_message('Paragraphs not allowed in letters',linenumber)
		else:
			tex_body.write('\paragraph{'+sentence[6:][:-1]+'}\n')
	elif sentence[7]!='#':
		if doc_class=='letter':
			error_message('Subparagraphs not allowed in letters',linenumber)
		else:
			tex_body.write('\subparagraph{'+sentence[7:][:-1]+'}\n')


def section_content(content):

	content = md_effect(content,'**','\\textbf{','}')
	content = md_effect(content,'*','\\textit{','}')
	content = md_effect(content,'<<','\\begin{flushleft}','\end{flusfleft}')
	content = md_effect(content,'>>','\\begin{flushright}','\end{flusfright}')
	content = md_effect(content,'==','\\begin{center}','\end{center}')


	while(content.find('![Alt text](')!=-1):
		add_package('','graphicx')
		content = content.replace('![Alt text](',' \\includegraphics{',1)
		content = content.replace(')','}',1)

	while(content.find('](')!=-1):
		add_package('','hyperref')
		label = content[content.find('[')+1:content.find(']')]
		link = content[content.find('(')+1:content.find(')')]
		content = content.replace(content[content.find('['):content.find(')')+1],'\href{'+link+'}{'+label+'}',1)
	
	while(content.find('~')!=-1):
		
		effect = content[content.find('~')+1:content.find(':')]
		effect = slicer(effect,' ')
		text = content[content.find(':')+1:content.find(':')+content[(content.find(':')+1):].find('~')+1]

		
		if(effect=='title'):
			if(bluntfile.find('~author')==-1):
				content = tilde_effect(content,'','','\\title{',text+'}\maketitle')
			else:
				content = tilde_effect(content,'','','\\title{',text+'}')
		
		elif(effect=='author'):
			content = tilde_effect(content,'','','\\author{',text+'}\maketitle')
			
		elif(effect=='date'):
			content = tilde_effect(content,'','','\date{',text+'}\maketitle')

		elif effect in zip(*effects_1)[0]:
			index = zip(*effects_1)[0].index(effect)
			content = tilde_effect(content,'',effects_1[index][2],effects_1[index][1],text+'}')
		
		elif effect in zip(*effects_2)[0]:
			index = zip(*effects_2)[0].index(effect)
			content = tilde_effect(content,'',effects_2[index][1],'\\begin{'+effect+'}',text+'\end{'+effect+'}')

		elif(effect in color):
			content = tilde_effect(content,'usenames,dvipsnames','color','\color{'+effect+'}{',text+'}')

		elif effect in zip(*maths)[0]:
			index = zip(*maths)[0].index(effect)
			content = tilde_effect(content,'','',maths[index][1],text+'}$')
		
		elif(effect in text_effect_array):
			content = tilde_effect(content,'','',text_effect_code[text_effect_array.index(effect)]+'{',text+'}')
		
		elif(effect in text_size_array):
			content = tilde_effect(content,'','','{'+text_size_code[text_size_array.index(effect)]+' ',text+'}')
			
		elif(effect=='import code'):
			
			if '.' in text:
				extension = text[text.find('.')+1:]
			else:
				error_message('No extension provided in file.',linenumber)
				break

			if(extension in code_extension_array):
				language = code_language_array[code_extension_array.index(extension)]
				content = tilde_effect(content,'','listings','{\lstset{language='+language+'}\lstinputlisting[frame=single]{',text+'}}')
			else:
				error_message('No .'+extension+' extension',linenumber)
				break
				
				
		elif(effect in letter_component_array and doc_class=='letter'):
			content = tilde_effect(content,'','',letter_component_code[letter_component_array.index(effect)]+'{',text+'}')
	
		
		elif(effect in frame_component_array and doc_class=='beamer'):
			content = tilde_effect(content,'','','\\'+effect+'{',text+'}')
		
		
		elif(effect in format_array and doc_class=='beamer'):
			if(text in format_options[format_array.index(effect)]):
				add_format(effect,text)
				content = content.replace('~','',1)
				content = content.replace(':','',1)
				content = content.replace(effect,'',1)
				content = content.replace(text,'',1)
			

		elif(effect in code_language_array):
			content = tilde_effect(content,'','listings','{\lstset{language='+effect+'}\\begin{lstlisting}[frame=single]',text+'\end{lstlisting}')
			

		elif(effect=='fraction'):
			index = text.find('/')
			if(index==-1):
				error_message('No / in a fraction',linenumber)
				break
			else:
				content = tilde_effect(content,'','','$\\frac{',text[:index]+'}{'+text[index+1:]+'}$')
					
		elif(effect=='square root' or effect=='sqrt'):
			content = tilde_effect(content,'','','$$\\sqrt{',text+'}$$')
			
		#HEXCOLOR RA 1,1,1

		else:
			error_message('No effect '+effect,linenumber)
			break

	tex_body.write(content)
	
	return content


#fixed
def md_effect(content,sign,begin,end):

	while(content.count(sign)>1):
		content=content.replace(sign,begin,1)
		content=content.replace(sign,end,1)

	return content


#semi-fixed
def tilde_effect(content,option,package,effect,text):

	if(package!=''):
		add_package(option,package)
		
	content = content.replace(content[content.find('~'):content.find(':')],effect,1)
	content = content.replace(content[content.find(':'):content.find('~')+1],text,1)
	
	return content




#fixed
def slicer(content,character):

	if character == ' ':
		character = '\s'

	regex = '^'+character+'*'
	content = re.sub(regex,'',content)
	regex = character+'*$'
	content = re.sub(regex,'',content)

	return content

#fixed
def add_package(option,package):

	package_virgin = True
	package = '\usepackage['+option+']{'+package+'}\n'

	tex.seek(0)
	if package in tex.readlines():
		package_virgin = False
	
	if(package_virgin):
		tex.write(package)

#fixed
def add_format(effect,option):

	tex.seek(0)
	format_virgin = True
	the_format = effect+'{'+option+'}\n'

	for line in tex.readlines():
		if(line==the_format):
			format_virgin = False
	
	if(format_virgin):
		tex.write(the_format)


#fixed
def table_effect(sentence):

	global nextsentence
	sentence = sentence.replace('|','&')
	nextsentence = nextsentence[:-1]+'|\n'

	if(not table_active):

		tex_body.write('\\begin{tabular}{')

		for i in range(0,column):
		
			alignment = 'l'
			counter = nextsentence.find('|')
			if(nextsentence[counter-1]==':'):
				alignment = 'r'
				if(nextsentence[0]==':'):
					alignment = 'c'
			tex_body.write('|'+alignment)
			nextsentence = nextsentence[(counter+1):]

		tex_body.write('|}\n\hline\n')

	tex_body.write(sentence[:-1]+'\\\\\n')
	
	if(not table_active):
		tex_body.write('\\hline\n')

	return True



#fixed
unordered_list_symbol = ['*','+','-']
def list_structure(sentence):

	global list_tab,list_active
	line_effect_virgin = True
	
	if sentence[:list_tab]=='\t'*list_tab and sentence[list_tab] in unordered_list_symbol and sentence[list_tab+1]==' ':
		list_active[list_tab] = order_list(sentence,'itemize')
		line_effect_virgin = False

	elif sentence[:list_tab]=='\t'*list_tab and re.match(r'([0-9]*).\s',sentence[list_tab:]):
		list_active[list_tab] = order_list(sentence,'enumerate')
		line_effect_virgin = False

	elif sentence[:(list_tab+1)]=='\t'*(list_tab+1) and sentence[list_tab+1] in unordered_list_symbol and sentence[list_tab+2]==' ':
		list_tab += 1
		list_active.append(False)
		list_active[list_tab] = order_list(sentence,'itemize')
		line_effect_virgin = False
	
	
	elif sentence[:(list_tab+1)]=='\t'*(list_tab+1) and re.match(r'([0-9]*).\s',sentence[list_tab+1:]):
		list_tab += 1
		list_active.append(False)
		list_active[list_tab] = order_list(sentence,'enumerate')
		line_effect_virgin = False

	elif(list_active[list_tab]):

		for i in range(0,list_tab+len(re.match(r'^\t*',sentence).group())+1):

			tex_body.write('\end{'+list_active[list_tab]+'}\n')
			list_active[list_tab] = False
			if list_tab>0:
				list_tab -= 1 
				list_active.pop()

		line_effect_virgin = list_structure(sentence)

	return line_effect_virgin


#fixed
def order_list(sentence,order):
	if not list_active[list_tab]:
		tex_body.write('\\begin{'+order+'}\n')
	tex_body.write('\item ' + sentence[(2+list_tab):])
		
	if not list_active[list_tab]:
		return order
	else:
		return list_active[list_tab]
	

	

#main

md = open(sys.argv[1],'r')
tex = open(sys.argv[2],'w+')
tex_body = open('latexbody.tex','w+')

tex.write('\documentclass[12pt]{'+doc_class+'}\n\n')
tex.write('%packages\n')

tex_body.write('\\begin{document}\n')

if(doc_class not in document_class_array):
	error_message('No document class named '+doc_class,None)
	exit()
	


bluntfile = md.read()
md.seek(0)
md_file = (md.readlines()+['\n'])




for sentence in md_file:

	linenumber += 1
	line_effect_virgin = True

	#

	if(sentence[0]=='#'):
		structure(sentence)
		line_effect_virgin = False
	
	#

	if(sentence.count('|') and line_effect_virgin):
		
		sentence = slicer(sentence[:-1],'\|')
		nextsentence = slicer(md_file[linenumber][:-1],'\|')
		
		if(table_head_active):
			line_effect_virgin = False
			if(sentence.count('-')):
				continue
			table_active = table_effect(sentence)

		elif(sentence.count('|')==nextsentence.count('|') and nextsentence.count('-')):
			line_effect_virgin = False
			column = nextsentence.count('|')+1
			table_active = table_head_active = table_effect(sentence)


	elif(table_active):

		tex_body.write('\hline\n\end{tabular}\n')
		table_active = table_head_active = False

	#
	
	if(line_effect_virgin):
		line_effect_virgin = list_structure(sentence)

	#
	if(line_effect_virgin):
		tex_body.write(sentence)
	
	#


tex_body.seek(0)
content = tex_body.read()
content = section_content(content)	
content = content+'\end{document}\n'

content.replace('\n','\\\\')
content.replace('\t','\indent')


tex_body.seek(0)
tex.write(content)


md.close()
tex.close()
tex_body.close()
os.system('rm latexbody.tex')

subprocess.check_output(['pdflatex -halt-on-error '+sys.argv[2]], shell=True)

if(program_error):
	print '\n...Converted With Error...\n'
else:
	print '\n...Converted Successfully...\n'

######END#########
