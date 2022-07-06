#Created by JoenTheWizard
"""
The functionality of this GUI application is to go through a wordlist of queries
and use the Google search API (provided with the 'googlesearch' module) and 
retrieve the responses. This application is good for the functionality of 
web scraping, a process of sending HTTP requests to retrieve data from a website.
A more applicable use of the program is scraping "dork" queries supported by Google's
search engine. Dorking is the process used to find specific keywords within a search
query. For example we can use dorking to find websites that are have certain keywords
in the url, description, html document etc. This would go through a wordlist of these
dorking queries and list about 10 of the results. Of course, sending too many requests
to Google would result in a HTTP Request Timeout (HTTP 429) and one could try and 
mitigate this by using a proxy server or by simply increasing the pause/delay between 
each request, which is provided within the application.
"""
import tkinter as tk
import threading
import requests as r
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
try:
    from googlesearch import search
except ImportError as e:
    print(e,"\nTry install module by 'pip install google' and try again (package also requires 'pip install beautifulsoup4'")
from datetime import datetime
from os import listdir
from os.path import isfile, join

#Set Pause Value between each query request
PAUSE_VAL = 40
#Set the Top-level Domain on Google Domains
TLD =  "com"
def SetPauseValue():
    def changeVal():
        global PAUSE_VAL
        PAUSE_VAL=int(T.get(1.0,END))
        pwind.destroy()
    pwind = Toplevel(window)
    pwind.title("Set Pause")
    pwind.resizable(0,0)
    pwind.geometry("300x70")
    L = Label(pwind,
          text ="Pause Value")
    T = Text(pwind, height=1,width=13)
    T.insert(1.0, str(PAUSE_VAL))
    L.pack()
    T.pack()
    B=Button(pwind, text="OK",command=changeVal).pack()

def SetTLD():
    def setTLD_b():
        global TLD
        TLD = opt.get()
        twind.destroy()
    twind = Toplevel(window)
    twind.title("Set TLD")
    twind.resizable(0,0)
    twind.geometry('300x90')
    L = Label(twind,text="TLD Value")
    options = []
    for m in r.get("https://www.google.com/supported_domains").text.split('\n'):
        if m != '':
            options.append(m.split('.google.')[1])
    opt = StringVar()
    opt.set(TLD)
    drop = OptionMenu(twind,opt,*options)
    L.pack()
    drop.pack()
    Confirm = Button(twind, text="OK",command=setTLD_b).pack()

def SendCmdBoxMsg(msg):
    cmdline.TextBox.insert('end',msg)
    cmdline.TextBox.see(END)

def BeginScanning():
    index = 0
    txtOut.TextBox.delete(1.0,END)
    SendCmdBoxMsg('[{0}] Beginning Scan... please wait!\n'.format(
             datetime.now().strftime("%H:%M:%S")))
    for lm in str(txtIn.TextBox.get(1.0,END)).split('\n'):
        if lm != '':
            try:
                txtOut.TextBox.insert(END,'{0}\n{1}\n'.format(lm,'-'*25))
                j = 1
                for sr in search(lm,tld=TLD,num=10,stop=10,pause=PAUSE_VAL):
                    txtOut.TextBox.insert(END,'{0}. {1}\n'.format(str(j),sr))
                    j += 1
            except Exception as e:
                SendCmdBoxMsg('[{0}] There was an error with sending this request: {1}\n'.format(
                datetime.now().strftime("%H:%M:%S"),
                str(e)
                ))
    SendCmdBoxMsg('[{0}] Scanning complete!\n'.format(
            datetime.now().strftime("%H:%M:%S")
        ))

CURRFILE = None
class FileOptions():
    def openFile(txtbox):
        global CURRFILE
        if CURRFILE is not None:
            for i in tree.get_children():
                tree.delete(i)
        filename = filedialog.askopenfilename(
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
        CURRFILE = filename
        txtbox.delete(1.0,"end")
        txtbox.insert(1.0,open(CURRFILE,'r').read())
        window.title('Python GUI application - {0}'.format(CURRFILE))
        SendCmdBoxMsg('[{0}] Opened file: {1}\n'.format(
            datetime.now().strftime("%H:%M:%S"),
            CURRFILE
        ))
        if CURRFILE is not None:
            path = '/'.join(CURRFILE.split('/')[:-1])
            tree.heading('file',text=path)
            for k in [f for f in listdir(path) if isfile(join(path, f))]:
                tree.insert('',END,values=k,tags=path)
    def saveAsFile(txtbox):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None:
            return
        CURRFILE = f.name
        window.title('Python GUI application - {0}'.format(CURRFILE))
        f.write(str(txtbox.get(1.0,END)))
        f.close()
        cmdline.TextBox.insert('end','[{0}] Successfully saved file: {1}\n'.format(
            datetime.now().strftime("%H:%M:%S"),
            CURRFILE
        ))
    def saveFile(txtbox):
        if CURRFILE is not None:
            f=open(CURRFILE, 'a')
            f.write(str(txtbox.get(1.0,END)))
            f.close()
            cmdline.TextBox.insert('end','[{0}] Saved file: {1}\n'.format(
                datetime.now().strftime("%H:%M:%S"),
                CURRFILE
            ))
    def newFile(txtBoxIn,txtBoxOut):
        global CURRFILE
        CURRFILE = None
        txtBoxIn.delete(1.0,"end")
        txtBoxIn.insert(1.0,'Input here')
        txtBoxOut.delete(1.0,"end")
        txtBoxOut.insert(1.0,'Output here')
        window.title('Python GUI application - New')
        cmdline.TextBox.insert('end','[{0}] Set new file\n'.format(
                datetime.now().strftime("%H:%M:%S"),
            ))
        cmdline.TextBox.see(END)
        if CURRFILE is None:
            for i in tree.get_children():
                tree.delete(i)
            tree.heading('file',text='Files')

class SetTextBox():
    def __init__(self, window, w_height, w_width):
        self.TextBox = Text(window, height=w_height, width=w_width)
    def SetTextConfigs(self,row,column,paddingx,paddingy,msg=None):
        self.TextBox.insert('end',msg if msg is not None else '')
        self.TextBox.grid(row=row,column=column,padx=paddingx,pady=paddingy)
    def retrieveValue(self):
        return self.TextBox.get("1.0",'end-1c')
        
def item_selected(event):
    global CURRFILE
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        record = "".join(item['values'])
        path = "".join(item['tags'])
        selec = f'{path}/{record}' 
        with open(selec,'r') as fl:
            txtIn.TextBox.delete(1.0,"end")
            txtIn.TextBox.insert(1.0,fl.read())
            CURRFILE = selec
            window.title('Python GUI application - {0}'.format(CURRFILE))
            cmdline.TextBox.insert('end','[{0}] Opened file: {1}\n'.format(
            datetime.now().strftime("%H:%M:%S"),
            CURRFILE
            ))
            cmdline.TextBox.see(END)


#Initialize the root window environment
window = tk.Tk()
window.geometry('700x700')
window.resizable(0,0)
window.title('Python GUI application - New')
window.background = '#3b3b3b'

#Text box that takes inputs (input box)
txtIn = SetTextBox(window,26,40)
txtIn.SetTextConfigs(1,1,5,2,'Input here')

#Text box that outputs from the inputs
txtOut = SetTextBox(window,26,40)
txtOut.SetTextConfigs(1,2,5,2,'Output here')

#small command-line environment 
cmdline = SetTextBox(window,13,40)
cmdline.SetTextConfigs(2,1,5,0)

tree = ttk.Treeview(window, columns=('file'),show='headings')
tree.heading('file',text='Files')
tree.grid(row=2,column=2)

tree.bind('<<TreeviewSelect>>', item_selected)

#Tkinter menu bar (File bar)
menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=lambda:FileOptions.newFile(txtIn.TextBox,txtOut.TextBox))
filemenu.add_command(label="Open", command=lambda:FileOptions.openFile(txtIn.TextBox)) #txtIn.TextBox.insert('end',open('a.txt','r').read())
filemenu.add_command(label="Save", command=lambda:FileOptions.saveFile(txtOut.TextBox))
filemenu.add_command(label="Save As", command=lambda:FileOptions.saveAsFile(txtOut.TextBox))
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)
#Run program. we create another thread seperate from the main thread for the scanning
#process
def scan_th():
    th=threading.Thread(target=BeginScanning)
    th.start()
optmenu = Menu(menubar, tearoff=0)
optmenu.add_command(label="Change request delay",command=SetPauseValue)
optmenu.add_command(label="Change TLD (Top-level Domain)",command=SetTLD)
menubar.add_cascade(label="Options",menu=optmenu)
menubar.add_command(label="Run",command=scan_th)
#Set the window configs
window.config(menu=menubar)
window.mainloop()