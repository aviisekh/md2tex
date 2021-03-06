#!/usr/bin/env python
import Tkinter
import tkMessageBox
from Tkinter import *
import tkFileDialog
from tkFileDialog import askopenfilename
import os,sys,subprocess
from PIL import ImageTk, Image

app = Tkinter.Tk()
app.title('md2tex Converter')
app.configure(background = 'lightblue')
app.attributes('-zoomed', True)
#abc=Tkinter.StringVar()
selected = None

def beenclicked():
	tex_text.delete('1.0', END)
	md_content = md_text.get('1.0',END)
	md_file = open('temp','w')
	md_file.write(md_content)
	md_file.close()
	
	if selected==None:
		doc_class="article"
	else:
		doc_class=selected

	try:
		msg = subprocess.check_output(['python cli.py temp latex.tex '+doc_class], shell=True)
	except Exception:
		msg = 'Error!!!'
	tkMessageBox.showinfo(title='compiling', message = msg)
	tex_text.insert(INSERT,open('latex.tex').read())
	os.remove("latex.tex")
	os.remove("temp")



class Cancel(Exception):
    pass
    
def docclass():
	
		app2= Tkinter.Tk()
		app2.title("doc class")
		app2.geometry('200x250')
		list1= Tkinter.Listbox(app2)
		for item in ['article','ieeetran','proc','minimal','report','book','slides','memoir','letter','beamer']:
			list1.insert(END,item)
		def callback(*event):
			global selected
			selected=list1.get(list1.curselection()[0])	
		#	
			#print selected
			return selected
		
		#list1.bind("<<ListboxSelect>>",callback)
		list1.pack()
		list1.bind("<<ListboxSelect>>",callback)
		#print selected
		choose= Tkinter.Button(app2, text = "Ok",activebackground='blue', width = 5,command = app2.destroy).pack()
		#global selected
		return selected

	
def quit():
	#mexit =tkMessageBox.ask(title="quit",message="Are you sure you want to quit?")
	app.quit()
	return

def nopen():
	md_text.delete('1.0', END) 
	fin=open(tkFileDialog.askopenfilename(filetypes= (("md files","*.md"),("All files","*.*"))),'r')
	lines=fin.read()
	for line in lines:
		md_text.insert(INSERT,lines)
		return 

 	
def savemd():
      md = tkFileDialog.asksaveasfile(mode='w', defaultextension=".md")
      md_textsave = str(md_text.get(0.0,END))
      md.write(md_textsave)
      md.close()

def showpdf():
	filePath= askopenfilename() 
    	os.system("gnome-open "+os.path.basename(filePath))

def askyesnocancel(title=None, message=None, **options):
    import tkMessageBox
    s = tkMessageBox.Message(
        title=title, message=message,
        icon=tkMessageBox.QUESTION,
        type=tkMessageBox.YESNOCANCEL,
        **options).show()
    if isinstance(s, bool):
        return s
    if s == "cancel":
        raise Cancel
    return s == "yes"
 
def latextopdf():
	latex2pdff= askopenfilename() 
	now =  os.path.basename(latex2pdff)
	os.system("clear") 
	os.system('pdflatex -halt-on-error '+now)
	if open(now):
		tkMessageBox.showinfo(title="pdf generated!!!", message =  subprocess.check_output(['pdflatex -halt-on-error '+now], shell=True))
		print "success"
		os.system("gnome-open "+now[:-3]+'pdf')
		os.remove(now[:-3]+'aux')
		os.remove(now[:-3]+'log')
		
	else:
		os.system("clear") 
		print "Oh dear."

	
def savetex():

	tex = tkFileDialog.asksaveasfile(mode='w', defaultextension=".tex")
	abc=md_text.get("1.0",END)
	tkMessageBox.showinfo(title="saving tex file", message ="saved!!! :D")
	md_textsave = str(tex_text.get(0.0,END))
	tex.write(md_textsave)
	tex.write('\documentclass{article}\n \n \\begin{document}\n')
	tex.write(abc)
	tex.write('\n\n\end{document}\n')
	tex.close()
	   
def nNew():
	mlabel =Tkinter.Label(app,text="new").pack()
	md_text.delete('1.0', END) 
	tex_text.delete('1.0', END) 
	return

def help():
	app1 =Tkinter.Tk()
	app1.title("readme")
	app1.geometry('350x550')
	#text3 = Tkinter.Text(app1)
	#text3.pack(fill='both')
	olabel =Tkinter.Label(app1,text="**Markdown** allows you to write using an easy-to-read, easy-to-write plain text format, then convert it to structurally valid XHTML (or HTML) whereas **LaTeX** is a document preparation system and document markup language.\n USER GUIDE\n	bold=**text**\n italic *text* \n bullets:\n\t * text \n \t + text\n\t - text\n").pack()


	
	def fun1(event):
	    #label.config(text="^.^ ^.^")
		label.config(text=" $     $    $     $") 
		label2.config(text="   _           _  ") 
		
	
	def fun2(event):
	    	label.config(text=" ^     ^    ^     ^") 
		label2.config(text="   _           _   ") 
	 
	label=Tkinter.Label(app1,text=" ^     ^    ^     ^") 
	label2=Tkinter.Label(app1,text="   _           _   ") 
	
	label.bind("<Enter>", fun1)
	label.bind("<Leave>", fun2)
	label.pack()
	label2.bind("<Enter>", fun1)
	label2.bind("<Leave>", fun2)
	label2.pack()
	return
def both():
	tex_view_text.pack_forget()
	md_view_text.pack_forget()
	scrl.pack_forget()
	scrl2.pack_forget()
	scrl.pack(side="left",fill='y', expand='10')		
	md_text.pack(side='left',fill='both',padx=5,pady=5)
	tex_text.pack(side='right',fill='both',padx=5,pady=5)
	scrl2.pack(side="right",fill='y',expand='50')

def only_md():
	tex_view_text.pack_forget()
	md_view_text.pack_forget()
	tex_text.pack_forget()
	scrl2.pack_forget()
	md_text.pack_forget()
	scrl.pack_forget()
	scrl.pack(side=RIGHT,fill='y')
	md_view_text.pack(padx=55,side=LEFT)
	md_text.pack(side=LEFT,fill=BOTH,expand='100')
	
	
def only_tex():
	tex_view_text.pack_forget()
	md_view_text.pack_forget()
	tex_text.pack_forget()
	scrl2.pack_forget()
	md_text.pack_forget()
	scrl.pack_forget()
	scrl2.pack(side=RIGHT,fill='y')
	tex_view_text.pack(padx=55,side=LEFT)
	tex_text.pack(side=LEFT,fill=BOTH,expand='100')

# action-function for the Button: highlight all occurrences of string
def find():
	# remove previous uses of tag `found', if any
	md_text.tag_remove('found2', '1.0', END)

	# get string to look for (if empty, no searching)
	s = edit.get(  )
	if s:
		# start from the beginning (and when we come to the end, stop)
		#idx1 = '1.0'
		idx2 = '1.0'
		while True:
			# find next occurrence, exit loop if no more
			idx2 =  md_text.search(s, idx2, nocase=1, stopindex=END) 
			#idx1 =  tex_text.search(s, idx1, nocase=1, stopindex=END)
			#if not idx1 : break
			if not idx2 : break
			# index right after the end of the occurrence
			#lastidx1 = '%s+%dc' % (idx1, len(s))
			lastidx2 = '%s+%dc' % (idx2, len(s))
			# tag the whole occurrence (start included, stop excluded)
			md_text.tag_add('found2', idx2, lastidx2) 
			#tex_text.tag_add('found1', idx1, lastidx1) 
			
			# prepare to search for next occurrence
			#idx1 = lastidx1
			idx2 = lastidx2
			# use a red foreground for all the tagged occurrences
			#tex_text.tag_config('found1', foreground='red')
			md_text.tag_config('found2', foreground='red')
		# give focus back to the Entry field
		edit.focus_set(  )



#START!!!
#START!!!
#START!!!
#START!!!
#START!!!
#START!!!
#START!!!
#START!!!
#START!!!
#START!!!
#START!!!
#START!!!
#START!!!
#START!!!

newimg = ImageTk.PhotoImage(Image.open('pics/new.ico'))
lateximg = ImageTk.PhotoImage(Image.open('pics/latex.ico'))	
mdimg = ImageTk.PhotoImage(Image.open('pics/md1.ico'))	
openimg = ImageTk.PhotoImage(Image.open('pics/open1.ico'))	
doc= ImageTk.PhotoImage(Image.open('pics/docclas.gif'))	
gen = ImageTk.PhotoImage(Image.open('pics/ge.jpg'))
conv = ImageTk.PhotoImage(Image.open('pics/convert.gif'))
pdfimg = ImageTk.PhotoImage(Image.open('pics/pdf.gif'))
mdviewimg = ImageTk.PhotoImage(Image.open('pics/md.gif'))
texviewimg = ImageTk.PhotoImage(Image.open('pics/tex.gif'))	
bothimg = ImageTk.PhotoImage(Image.open('pics/both.gif'))	
	
run= Tkinter.Button(app, highlightbackground='lightblue',compound=CENTER,background = 'lightblue',text = "Generate LaTex code",activebackground='blue', width = 10,command = beenclicked).pack(side="top", fill='both')	
but_frame = Frame(app, bg="lightblue")



butt = Button(but_frame, text='Find',background = 'lightblue',command=find,activebackground='blue').pack(side=RIGHT)
edit = Entry(but_frame)
edit.pack(side=RIGHT)
edit.focus_set(  )
Label(but_frame,background = 'lightblue',text='Text to find:').pack(side=RIGHT)

Button(but_frame,compound=LEFT, highlightbackground='lightblue',background = 'lightblue',relief='flat',activebackground='blue',image =openimg,text= 'open',command = nopen).pack(side=LEFT)
Button(but_frame, relief='flat',compound=LEFT, highlightbackground='lightblue',background = 'lightblue',text = "save md",activebackground='blue', image =mdimg,command = savemd).pack(side=LEFT)
Button(but_frame, relief='flat',compound=LEFT,highlightbackground='lightblue',background = 'lightblue', text = "save tex",activebackground='blue', image =lateximg,command = savetex).pack(side=LEFT)
Button(but_frame,relief='flat',compound=LEFT,  highlightbackground='lightblue',background = 'lightblue',text = "docclass",activebackground='blue', image=doc,command = docclass).pack(side=LEFT)
Button(but_frame, relief='flat',compound=LEFT,highlightbackground='lightblue', background = 'lightblue',text = "pdfgenerate",activebackground='blue', image= conv,command = latextopdf).pack(side=LEFT)	
Button(but_frame, relief='flat',compound=LEFT, highlightbackground='lightblue',background = 'lightblue',text = "pdfshow",activebackground='blue', image=pdfimg,command = showpdf).pack(side=LEFT)
but_frame.pack(side=TOP,fill=X)

but_frame2 = Frame(app,height="16px")
but_frame2.configure(background = 'lightblue')

Label(but_frame2,highlightbackground='lightblue',background = 'lightblue').pack(side = RIGHT,padx=22,pady=6)
both_but = Button(but_frame2, compound=LEFT,highlightbackground='lightblue',background = 'lightblue',activebackground='blue', image =bothimg,command = both).pack(side=RIGHT,padx=5,pady=2)
tex_but = Button(but_frame2, compound=LEFT,highlightbackground='lightblue',background = 'lightblue', activebackground='blue', image =texviewimg,command = only_tex).pack(side=RIGHT,padx=5,pady=2)
md_but = Button(but_frame2,compound=LEFT,highlightbackground='lightblue',background = 'lightblue', activebackground='blue',image =mdviewimg,command = only_md).pack(side=RIGHT,padx=5,pady=2)

Label(but_frame2,background = 'lightblue',text= "View:  ").pack(side = RIGHT,padx=5)
Label(but_frame2,highlightbackground='lightblue',background = 'lightblue',text= "md2tex converter").pack(side = LEFT)

but_frame2.pack(side=BOTTOM,fill=X)
but_frame2.pack_propagate(False)
	
menubar = Tkinter.Menu(app,background = 'lightblue')
filemenu =Tkinter. Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=nNew)
filemenu.add_command(label="Open", command=nopen)
filemenu.add_command(label="Docclass", command=docclass)
filemenu.add_command(label="pdf generate", command=latextopdf)
filemenu.add_command(label="pdf show", command=showpdf)
filemenu.add_command(label="Save md file", command=savemd)
filemenu.add_command(label="Save tex file. ..", command=savetex)
filemenu.add_command(label="Close", command=quit)
menubar.add_cascade(label="File", menu=filemenu,activebackground='blue',background = 'lightblue')


helpmenu = Tkinter.Menu(menubar, tearoff=0,background = 'lightblue')

helpmenu.add_command(label="documentation", command=help)
helpmenu.add_command(label="About...", command=help)
menubar.add_cascade(label="Help", menu=helpmenu,activebackground='blue',background = 'lightblue')

app.config(menu= menubar,background = 'lightblue')



md_text = Tkinter.Text(app,background = 'lightblue')
var = StringVar()

def get_position(event):
    """get the line and column number of the text insertion point"""
    line, column = md_text.index('insert').split('.')
    s = "line=%s  column=%s" % (line, column)
    var=s 
    app.title(s)
     
md_text.bind("<KeyRelease>", get_position)


def select_all2(event):
        md_text.tag_add(SEL, "1.0", END)
        md_text.mark_set(INSERT, "1.0")
        md_text.see(INSERT)
	return 'break'

md_text.config(
    borderwidth=0,
    font="{Lucida Sans Typewriter} 12",
    foreground="green",
    background="white",
    insertbackground="black", # cursor
    #selectbackground="lightblue",
    wrap=WORD, # use word wrapping
    width=54,
    undo=True, 
    border = 3,
    highlightthickness=1,
    highlightbackground='lightblue' # Tk 8.4
    )
#img=ImageTk.PhotoImage(Image.open('pics/images.jpg'))	
#md_text.insert(END,'\n')
#md_text.image_create(END, image=img)
md_text.bind("<Control-Key-a>", select_all2)
md_text.bind("<Control-Key-A>", select_all2) 

	

md_view_text = Label(but_frame,bg='lightblue',fg = 'red',text= "Md view  ")

tex_text = Text(app)
tex_view_text = Label(but_frame,bg='lightblue',fg = 'blue',text= "Tex view  ")
tex_text.config(
    borderwidth=0,
    font="{Lucida Sans Typewriter} 12",
    foreground="black",
    background="white",
    insertbackground="black", # cursor
    #selectbackground="lightblue",
    wrap=WORD, # use word wrapping
    width=54,
    undo=True,
    border = 3,
    highlightbackground='lightblue',
    highlightthickness=1 
  # Tk 8.4
    )

def select_all(event):
	tex_text.tag_add(SEL, "1.0", END)
	tex_text.mark_set(INSERT, "1.0")
	tex_text.see(INSERT)
	return 'break'

tex_text.bind("<KeyRelease>", get_position)	
tex_text.bind("<Control-Key-a>", select_all)
tex_text.bind("<Control-Key-A>", select_all) 
def get_position_tex(event):
    """get the line and column number of the text insertion point"""
    line, column = tex_text.index('insert').split('.')
    s = "line=%s  column=%s" % (line, column)
    var=s 
    app.title(s)
     
tex_text.bind("<KeyRelease>", get_position_tex)

scrl = Tkinter.Scrollbar(app, command=md_text.yview,background = 'lightblue',highlightbackground='lightblue')
md_text.config(yscrollcommand=scrl.set)

scrl2 =Tkinter. Scrollbar(app, command=tex_text.yview,background = 'lightblue',highlightbackground='lightblue')
tex_text.config(yscrollcommand=scrl2.set)


def file_new(event=None):
    try:
        md_text.clear()
    except Cancel:
        pass
    return "break" # don't propagate events

def file_open(event=None):
    try:
        save_if_modified()
        open_as()
    except Cancel:
        pass
    return "break"

def file_save(event=None):
    try:
        savemd()
    except Cancel:
        pass
	tkMessageBox.showinfo(title="saving md file", message ="saved!!! :D")
    return "break"



def file_save1(event=None):
    try:
        savetex()
    except Cancel:
        pass
	tkMessageBox.showinfo(title="saving tex file", message ="saved!!! :D")
    return "break"



def file_quit(event=None):
    app.quit()



scrl.pack(side="left",fill='y', expand='10')		
md_text.pack(side='left',fill='both',padx=5,pady=5)
tex_text.pack(side='right',fill='both',padx=5,pady=5)
scrl2.pack(side="right",fill='y',expand='50')


md_text.bind("<Control-n>", file_new)
md_text.bind("<Control-o>", file_open)
md_text.bind("<Control-s>", file_save)
md_text.bind("<Control-q>", file_quit)

tex_text.bind("<Control-s>", file_save1)
tex_text.bind("<Control-q>", file_quit)

app.protocol("WM_DELETE_WINDOW", file_quit)

app.mainloop()
