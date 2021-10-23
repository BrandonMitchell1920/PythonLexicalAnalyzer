# +----------------------------------------------------------------------------
#
# Name:     Brandon Mitchell
# Description:  The GUI code.  A lot of stuff has to be repeated simply because
#               I have to do the same code for each button and so on.  The GUI
#               is a class so various functions can easily share state.  
#               However, only one instance should ever be created.
#
#               I seperated the lexical analyzer and the GUI like this as it 
#               should make translating a little easier as I don't have a bunch
#               of intercoupled functions, just a lexical anaylzer and the GUI
#               that accesses it through its interface.
#
# +----------------------------------------------------------------------------

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

# +----------------------------------------------------------------------------

"""
    brief:  Displays an error used by the main function, informs user of 
            missing files
    pre:    Only meant to be used and then immedientely end program, don't use
            with GUI
"""
def missingFilesError():
    root = Tk()
    root.withdraw()
    messagebox.showerror(title = " Missing Files! ", message = "One or more " \
        "default files are missing!  Ensure all tables and the default " \
        "test file exist.")

"""
    Class for managing the GUI and its state.  Majority of functions are 
    "private", signified with an _ to start their name.  User should create by
    passing in a Lex object and then call its mainloop function to start it.
"""
class GUI:
    
    # Static constants for directories    
    DEF_TABLE_DIR = "tables"
    DEF_SOURCE_DIR = "testFiles"
    
    DEF_SCAN = DEF_TABLE_DIR + "/DefaultScanTable.csv"
    DEF_TOKEN = DEF_TABLE_DIR + "/DefaultTokenTable.csv"
    DEF_KEY = DEF_TABLE_DIR + "/DefaultKeywordTable.csv"
    DEF_SOURCE = DEF_SOURCE_DIR + "/DefaultTestFile.c"

    FILES_SUPPORTED = [("CSV Files", "*.csv"), ("All Files", "*")]



    """
        brief:  Called upon creation to set up the main output window
        pre:    self.root must have already been created
        post:   The self.outText attribute has been created
    """
    def _creatOutText(self):
    
        # Create the text and bind the keyboard commands to it
        self.outText = Text(self.root, width = 40, height = 24, wrap = "word", \
            padx = 10, pady = 10, borderwidth = 10, relief = "sunken")
        self.outText.bind("<Key>", lambda event: self._copyManager(event))
        self.outText.bind("<Control-w>", lambda event: self.root.destroy())

        # Create a scroll bar
        yScroll = ttk.Scrollbar(self.root, orient = 'vertical', command = \
            self.outText.yview)
        self.outText["yscrollcommand"] = yScroll.set
        
        label = Label(self.root, text = "Output Panel")
        
        # Position the elements in the window
        label.grid(column = 0, row = 0)
        self.outText.grid(column = 0, row = 1, rowspan = 100, sticky = 'nwes')
        yScroll.grid(column = 1, row = 1, rowspan = 100, sticky = 'ns')  



    """
        brief:  Creates the menu bar and binds various commands to the options
        pre:    self.root must have already been created
        post:   A menu bar has been created in the window
    """
    def _createMenuBar(self):
        menuBar = Menu(self.root, tearoff = 0)
        
        # Adds various options for opening and saving files as well as ending 
        # the program
        fileMenu = Menu(menuBar, tearoff = 0);
        fileMenu.add_command(label = "  Open Scan Table ...", command = \
            lambda: self._openScanTable())    
        fileMenu.add_command(label = "  Open Token Table ...", command = \
            lambda: self._openTokenTable())
        fileMenu.add_command(label = "  Open Keyword Table ...", command = \
            lambda: self._openKeywordTable())
        fileMenu.add_command(label = "  Open Source File ...", command = \
            lambda: self._openSourceCode())
        fileMenu.add_separator()
        fileMenu.add_command(label = "  Save Output ...", command = \
            lambda: self._saveOutText())
        fileMenu.add_separator()
        fileMenu.add_command(label = "  Exit", command = self.root.destroy)
        
        # Option to for user to clear output
        editMenu = Menu(menuBar, tearoff = 0)
        editMenu.add_command(label = "  Clear Output", command = lambda: \
            self.outText.delete("1.0", END))

        # Options for scanning
        scanMenu = Menu(menuBar, tearoff = 0)
        scanMenu.add_command(label = "  Next Token", command = lambda: \
            self._scanManager())
        scanMenu.add_command(label = "  Auto Scan", command = lambda: \
            self._autoScanManager())
        scanMenu.add_command(label = "  Restart Scanning", command = lambda: \
            self.lex.restartIndex())

        # Shows my copyright window so you know I didn't steal this and that
        # other people did!
        helpMenu = Menu(menuBar, tearoff = 0)
        helpMenu.add_command(label = "  About ...", command = lambda:
            messagebox.showinfo(" Info ", "Copyright (C) Brandon Mitchell, " + \
            "2021, All Rights Reserved\nCSCI 305, Programming Languages, F21"))
     
        # Adds all submenus into the main menuBar
        menuBar.add_cascade(label = "File", menu = fileMenu)
        menuBar.add_cascade(label = "Edit", menu = editMenu)
        menuBar.add_cascade(label = "Scan", menu = scanMenu)
        menuBar.add_cascade(label = "Help", menu = helpMenu)
       
        self.root.config(menu = menuBar)



    """
        brief:  Creates various text boxes, labels, and buttons for managing
                the different tables
        pre:    self.root must have already been created
        post:   Various text boxes, labels, and buttons are added to window, 
                self.scanTableText, self.tokenTableText, self.keywordTableText,
                and self.sourceCodeText
    """
    def _createTablesInfoPanel(self):
        
        # Creates the panels for the Scan Table, self.scanTableText is created
        # as an attribute
        scanTableLabel = Label(self.root, text = "Scan Table")
        
        self.scanTableText = Text(self.root, width = 35, height = 1, \
            padx = 2, pady = 2, borderwidth = 2, relief = "sunken")
            
        # Bind all keys to a special function to make text read only, allow
        # ctrl-w through to kill program
        self.scanTableText.bind("<Key>", lambda event: \
            self._copyManager(event))
        self.scanTableText.bind("<Control-w>", lambda event: \
            self.root.destroy())
         
        # Split the text at the / so only the filename is shown
        self.scanTableText.insert("1.0", GUI.DEF_SCAN.split('/')[-1])
        
        # Opens a file dialog and then passes the file to self.lex for reading 
        scanTableButton = Button(self.root, text = "Browse", command = \
            lambda: self._openScanTable())
        
        # Positions elements in the window using grid()
        scanTableLabel.grid(column = 2, row = 1)
        self.scanTableText.grid(padx = 20, column = 2, row = 2, columnspan = 3)
        scanTableButton.grid(padx = 20, column = 5, row = 2)
        
        # Creates the panels for the Token Table, self.tokenTableText is 
        # created as an attribute, else is the same as above
        tokenTableLabel = Label(self.root, text = "Token Table")

        self.tokenTableText = Text(self.root, width = 35, height = 1, \
            padx = 2, pady = 2, borderwidth = 2, relief = "sunken")
        self.tokenTableText.bind("<Key>", lambda event: \
            self._copyManager(event))
        self.tokenTableText.bind("<Control-w>", lambda event: \
            self.root.destroy())
        self.tokenTableText.insert("1.0", GUI.DEF_TOKEN.split('/')[-1])
        
        tokenTableButton = Button(self.root, text = "Browse", command = \
            lambda: self._openTokenTable())
        
        tokenTableLabel.grid(column = 2, row = 15)
        self.tokenTableText.grid(padx = 20, column = 2, row = 16, \
            columnspan = 3)
        tokenTableButton.grid(padx = 20, column = 5, row = 16)
        
        # Creates the panels for the Keyword Table, self.keywordTableText is 
        # created as an attribute, else is the same as above
        keywordTableLabel = Label(self.root, text = "Keyword Table")
        
        self.keywordTableText = Text(self.root, width = 35, height = 1, \
            padx = 2, pady = 2, borderwidth = 2, relief = "sunken")
        self.keywordTableText.bind("<Key>", lambda event: \
            self._copyManager(event))
        self.keywordTableText.bind("<Control-w>", lambda event: \
            self.root.destroy())
        self.keywordTableText.insert("1.0", GUI.DEF_KEY.split('/')[-1])
        
        keywordTableButton = Button(self.root, text = "Browse", command = \
            lambda: self._openKeywordTable())
        
        keywordTableLabel.grid(column = 2, row = 29)
        self.keywordTableText.grid(padx = 20, column = 2, row = 30, \
            columnspan = 3)
        keywordTableButton.grid(padx = 20, column = 5, row = 30)        
        
        # Creates the panels for the Source Code, self.sourceCodeText is 
        # created as an attribute, else is the same as above
        sourceCodeLabel = Label(self.root, text = "Source Code")
        
        self.sourceCodeText = Text(self.root, width = 35, height = 1, \
            padx = 2, pady = 2, borderwidth = 2, relief = "sunken")
        self.sourceCodeText.bind("<Key>", lambda event: \
            self._copyManager(event))
        self.sourceCodeText.bind("<Control-w>", lambda event: \
            self.root.destroy())
        self.sourceCodeText.insert("1.0", GUI.DEF_SOURCE.split('/')[-1])
        self.outText.insert(END, "~ {} ~\n".format(GUI.DEF_SOURCE \
            .split('/')[-1]))
        
        sourceCodeButton = Button(self.root, text = "Browse", command = \
            lambda: self._openSourceCode())
        
        sourceCodeLabel.grid(column = 2, row = 43)
        self.sourceCodeText.grid(padx = 20, column = 2, row = 44, \
            columnspan = 3)
        sourceCodeButton.grid(padx = 20, column = 5, row = 44)    



    """
        brief:  Creates various buttons for scanning, binds functions to them
        pre:    Several buttons are created in the window
    """
    def _createScanControls(self):    
        scanControlLabel = Label(self.root, text = "Scan Controls")
        
        # Create the step by step button, bind the enter key to it
        scanControlButton = Button(self.root, text = "Next Token", command = \
            lambda: self._scanManager())
        self.root.bind("<Return>", lambda event: self._scanManager())
        
        # The auto-scan button
        autoScanButton = Button(self.root, text = "Auto Scan", command = \
            lambda: self._autoScanManager())

        # Sets the locations of elements
        scanControlLabel.grid(column = 2, row = 70)
        scanControlButton.grid(padx = 20, column = 3, row = 70)    
        autoScanButton.grid(padx = 20, column = 4, row = 70)



    """
        brief:  Calls the lexical analyzer to get the next token, may call 
                several times to ignore comments, informs user when eof hit
        param:  warn: bool, default value of True, just to help auto scan deal
                with the comment is last token edge case
        pre:    self.outText must have been created, self.lex must have files
                loaded
        post:   self.outText is updated if necessary
    """
    def _scanManager(self, warn = True):
        
        # Don't bother continuing if eof has been hit
        if self.lex.eof():
            self._warnUserEofHit()
        
        else:
        
            # Get the token and keep getting tokens until it is something other
            # than whiteSpace or a comment or end-of-file is hit
            self.lex.getNextToken()
            while self.lex.curToken in {"whiteSpace", "comment"} and not \
                self.lex.eof():
                self.lex.getNextToken()
              
            # Some extra code for when the last token is a comment, only
            # happens if eof hit, warn specifically so autoScan doesn't mess
            # up the output
            if warn and self.lex.curToken == "comment":
                self._warnUserEofHit()
                
            # So the autoScan doesn't print out the last comment if it exists
            elif self.lex.curToken != "comment":
              
                if self.lex.errorFlag:
                    self.outText.insert(END, self.lex.errorMessage + '\n')
              
                else:
                    # "Print" out the token and lexemme
                    self.outText.insert(END, "Token: {:<12} Lexemme: {}\n" \
                        .format(self.lex.curToken, self.lex.curLexemme))

                # Scrolls the window down
                self.outText.see(END)



    """
        brief:  Simply keeps calling the lexical analyzer to read the whole 
                file automatically
        pre:    self.lex has no more tokens to give
    """
    def _autoScanManager(self):
        
        if not self.lex.eof():
        
            # Keep scanning until eof
            while not self.lex.eof():
                self._scanManager(False)
                
        else:
            self._warnUserEofHit()



    """
        brief:  Shows an info window warning the user that eof was hit
    """
    def _warnUserEofHit(self):
        messagebox.showinfo(" EOF Reached! ", "End-of-file reached!  No more " \
            "tokens to read!")



    """
        brief:  Warns the user with a messagebox that opening a new file will 
                restart scanning
        return: bool, True or False depending if yes or no
    """
    def _warnUserFileOpen(self):
        return messagebox.askyesno(title = " Restart Scanning? ", message = \
            "Opening a new file will restart scanning from the beginning.  " \
            "Do you wish to continue?")



    """
        brief:  Lets the user know that the file could not be opened.
    """
    def _errorUserFileError(self, fileName):
        messagebox.showerror(title = " Error Opening File!", message = \
            "\"{}\" could not be opened.  Ensure it exists and is of the " \
            "proper type (text files, not binary).".format(fileName))



    """
        brief:  Checks keyboard input and allows copying of text but not 
                modification, makes text read only
        params: event, the event that triggered the function call
        pre:    Any key was hit while element was selected
        post:   Text is copied to system clipboard if ctrl-c was hit
        return: "break" if not ctrl-c, else None
    """
    def _copyManager(self, event):

        # 12 means control was hit prior and 'c' is the char
        if event.state != 12 or event.keysym != 'c':
            return "break"



    """
        brief:  Creates a save file dialog so the user can save the ouput to a 
                file of their choosing
        pre:    self.outText must have already been created
        post:   File is saved to user's computer
    """
    def _saveOutText(self):
        fileName = filedialog.asksaveasfilename(title = " Save Output", 
            filetypes = [("Text File", "*.txt"), ("All Files", "*")],
            initialdir = "./", defaultextension = ".txt")
            
        # User canceled out, fileName is false
        if fileName:
        
            # Could potentially error, but the GUI will just keep chugging on
            with open(fileName, 'w') as file:
                file.write(self.outText.get("1.0", END))



    """
        brief:  Creates a file dialog and calls self.lex's appropriate method
        post:   self.scanTableText is updated
    """
    def _openScanTable(self):
        
        # Check if we are currenlty scanning and if so, warn user
        openNew = True
        if not self.lex.eof(): 
            openNew = self._warnUserFileOpen()
        
        # Continue if they want to open the file
        if openNew:
            fileName = filedialog.askopenfilename(title = " Choose a Scan " \
                "Table", initialdir = GUI.DEF_TABLE_DIR, filetypes = \
                GUI.FILES_SUPPORTED)   
                
            # No file chosen / user canceled process, fileName is false
            if fileName:
            
                # If we are able to open and read the file, update boxes
                if self.lex.readScanTable(fileName):
                    self.scanTableText.delete("1.0", END)
                    self.scanTableText.insert("1.0", fileName.split('/')[-1])
                    
                # File is too large, doesn't exist, or is not text data
                else:
                    self._errorUserFileError(fileName)



    """
        brief:  Creates a file dialog and calls self.lex's appropriate method
        post:   self.tokenTableText is updated
    """
    def _openTokenTable(self):
    
        # Check if we are currenlty scanning and if so, warn user
        openNew = True
        if not self.lex.eof(): 
            openNew = self._warnUserFileOpen()
        
        # Continue if they want to open the file
        if openNew:
            fileName = filedialog.askopenfilename(title = " Choose a Token " \
                "Table", initialdir = GUI.DEF_TABLE_DIR, filetypes = \
                GUI.FILES_SUPPORTED)   
            
            # No file chosen / user canceled process, fileName is false
            if fileName:
            
                # If we are able to open and read the file, update boxes
                if self.lex.readTokenTable(fileName):
                    self.tokenTableText.delete("1.0", END)
                    self.tokenTableText.insert("1.0", fileName.split('/')[-1]) 
                
                # File is too large, doesn't exist, or is not text data
                else:
                    self._errorUserFileError(fileName)



    """
        brief:  Creates a file dialog and calls self.lex's appropriate method
        post:   self.keywordTableText is updated
    """
    def _openKeywordTable(self):
    
        # Check if we are currenlty scanning and if so, warn user
        openNew = True
        if not self.lex.eof(): 
            openNew = self._warnUserFileOpen()
    
        # Continue if they want to open the file
        if openNew:
            fileName = filedialog.askopenfilename(title = " Choose a Keyword " \
                "Table", initialdir = GUI.DEF_TABLE_DIR, filetypes = \
                GUI.FILES_SUPPORTED)   
                
            # No file chosen / user canceled process, fileName is false
            if fileName:
                
                # If we are able to open and read the file, update boxes
                if self.lex.readKeywordTable(fileName):
                    self.keywordTableText.delete("1.0", END)
                    self.keywordTableText.insert("1.0", fileName.split('/')[-1])
                
                # File is too large, doesn't exist, or is not text data
                else:
                    self._errorUserFileError(fileName)



    """
        brief:  Creates a file dialog and calls self.lex's appropriate method
        post:   self.sourceCodeText is updated
    """
    def _openSourceCode(self):
    
        # Check if we are currenlty scanning and if so, warn user
        openNew = True
        if not self.lex.eof(): 
            openNew = self._warnUserFileOpen()
        
        # Continue if they want to open the file
        if openNew:
            fileName = filedialog.askopenfilename(title = " Choose a Source " \
                "Code File", initialdir = GUI.DEF_SOURCE_DIR)   
                
            # No file chosen / user canceled process, fileName is false
            if fileName:
            
                # If we are able to open and read the file, update boxes
                if  self.lex.readSourceCode(fileName):
                    self.sourceCodeText.delete("1.0", END)
                    self.sourceCodeText.insert("1.0", fileName.split('/')[-1])
                    self.outText.insert(END, "\n~ {} ~\n".format(fileName \
                        .split('/')[-1]))
                    self.outText.see(END)
        
                # File is too large, doesn't exist, or is not text data
                else:
                    self._errorUserFileError(fileName)



    """
        brief:  Constructor
        params: lexicalAnalyzer: Lex, a Lex object
        pre:    lexicalAnalyzer is assumed to have already opened all necessary
                files
    """
    def __init__(self, lexicalAnalyzer):
        
        self.lex = lexicalAnalyzer
        
        self.root = Tk()
        self.root.title(" Lexical Analyzer (Python Ver.) ")
        self.root.iconbitmap("icon/A Pumpkin For All Seasons.ico")
        self.root.bind("<Control-w>", lambda event: self.root.destroy())
        
        # Creates output window, self.outText
        self._creatOutText()
        
        # Creates the menu bar, doesn't create an attribute
        self._createMenuBar()
        
        # Creates the info panels, self.scanTableText, self.tokenTableText,
        # self.keywordTableText, and self.sourceCodeText
        self._createTablesInfoPanel()
        
        # Cretes the controls for scanning the file
        self._createScanControls()
        
        self.root.grid_columnconfigure(0, weight = 1)
        self.root.grid_rowconfigure(0, weight = 1)



    """
        brief:  Starts the GUI, only "public" method
    """
    def mainloop(self):
        self.root.mainloop()
