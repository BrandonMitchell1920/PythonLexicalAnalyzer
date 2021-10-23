# +----------------------------------------------------------------------------
#
# Name:     Brandon Mitchell
# Description:  The lexical analyzer, meant to be used with a front end, like
#               GUI, won't output any thing by itself.  Needs all tables and a
#               source file to run.  I used the book example for help, but I 
#               modified it to read comments and white space and I just leave
#               to the front end not to output them.  I removed the "recover"
#               error handling that the psuedocode had as I didn't think it was
#               all that useful.  The error messages in the token table seem a 
#               whole lot more useful and doesn't require any special parsing.
#
# +----------------------------------------------------------------------------

"""
    brief:  Reads in CSV files
    params: delim: string, the delimiter to use, defaults to comma
    return: A 2D matrix of strings
"""
def csvReader(fileName, delim = ','):

    # Read whole file, split at newlines, and then split at commas
    with open(fileName) as f:
        text = [line.split(delim) for line in f.read().split('\n')]
    return text

"""
    Lexical analyzer class, requires three tables and source code program to
    run, will use info in tokenTable to give useful errors, only reads one
    token at a time and will not throw out whiteSpace and comments.
"""
class Lex:

    """
        brief:  Looks into the scanning table to return the proper action
        pre:    Assumes tables exist and are properly loaded
        return: string, the state to move to, either '-' or a number string
    """
    def _findAction(self, curChar, curState):
        
        # Character stored in table as int, best way to represent without any
        # issues arising from escape sequences or tabs and the like
        charVal = str(ord(curChar))
        
        if charVal in self._scanTable[0]:
            colVal = self._scanTable[0].index(charVal)
            return self._scanTable[curState][colVal]
        
        return '-'



    """
        brief:  Creates the error message and sets and clears appropriate 
                values
        params: tok: string, the error from the token table
        params: image: string, the image when the error occured
        params: curChar: char, the current character that caused the error
        post:   Sets error flag and message, clears token and lexemme
    """
    def _handleError(self, tok, image, curChar):
        self.errorFlag = True
        
        # Add curChar to image, but call string to remove whiteSpace if it was
        # a new line character
        self.errorMessage = "{}: {}".format(tok, ("".join(image) + curChar) \
            .strip())
        
        self.curToken = ""
        self.curLexemme = ""



    """
        brief:  Constructor
    """
    def __init__(self):
    
        # Tables and source code
        self._scanTable = [[]]
        self._tokenTable = []
        self._keywordTable = {}
        self._sourceFile = ""
        
        self._index = 0
        
        self.curToken = ""
        self.curLexemme = ""
        
        # Used in handling errors
        self.errorFlag = False
        self.errorMessage = ""



    """
        brief:  Reads in the appropriate table
        post:   The appropriate attribute is modified and index starts over
                only if reading suceeds
        return: bool, True or False if the reading succeeded
    """
    def readScanTable(self, fileName):
        try:
        
            # In try in case file is too large, invalid data, doesn't exist
            newTable = csvReader(fileName)
            self._index = 0
            self._scanTable = newTable
            return True
        except:
            return False



    """
        brief:  Reads in the appropriate table
        post:   The appropriate attribute is modified and index starts over
                only if reading suceeds
        return: bool, True or False if the reading succeeded
    """
    def readTokenTable(self, fileName):
        try:
        
            # In try in case file is too large, invalid data, doesn't exist
            newTable = csvReader(fileName)
            self._index = 0        

            # Converts 2D matrix to a 1D list
            self._tokenTable = [word[0] for word in newTable]
            return True
        except:
            return False



    """
        brief:  Reads in the appropriate table
        post:   The appropriate attribute is modified and index starts over
                only if reading suceeds
        return: bool, True or False if the reading succeeded
    """
    def readKeywordTable(self, fileName):
        try:
        
            # In try in case file is too large, invalid data, doesn't exist
            newTable = csvReader(fileName)
            self._index = 0
            
            # Converts to a set of keywords
            self._keywordTable = {word[0] for word in newTable}
            return True
        except:
            return False



    """
        brief:  Reads in the appropriate table
        post:   The appropriate attribute is modified and index starts over
                only if reading suceeds
        return: bool, True or False if the reading succeeded
    """
    def readSourceCode(self, fileName):
        try:
        
            # In try in case file is too large, invalid data, doesn't exist
            with open(fileName) as file:
            
                # Remove white space from front and end
                newFile = file.read().strip()
                
            self._index = 0
            self._sourceFile = newFile
            return True
        except:
            return False 



    """
        brief:  Returns true if end-of-file has been reached
        return: True or False to indicate if end-of-file was hit
    """
    def eof(self):
        return self._index >= len(self._sourceFile)



    """
        brief:  Sets the index into the file to 0, allows for scanning to 
                restart from the beginning.
        post:   self._index is set to 0
    """
    def restartIndex(self):
        self._index = 0



    """
        brief:  The actual scanning code
        pre:    Assumes all tables and files have been read in properly
        post:   Updates various attributes depending on if a recognize or error
                state occured
    """
    def getNextToken(self):

        # Don't bother exectuing any code below if eof was hit
        if self.eof(): return
        
        self.errorFlag = False
        self.errorMessage = ""
        
        tok = ""
        curChar = ""
        
        image = []
        
        # The default start state, 0 is invalid, impossible state
        curState = 1
        
        # Might be frowned upon, but throwing an extra variable into the mix
        # and then having to check it several times will just muddy this
        while True:
            
            # End of file is a possible delimter end for tokens
            if self.eof(): 
                tok = self._tokenTable[curState]
                
                # Recognize state, errors prepended with '-'
                if tok[0] != '-':
                    break
                    
                # Error state
                else:
                    self._handleError(tok, image, '')
                    return
                    
            curChar = self._sourceFile[self._index]
            self._index += 1
            
            action = self._findAction(curChar, curState)
            
            # Move state
            if action != '-':
                curState = int(action)
                
            else:
                tok = self._tokenTable[curState]
                
                # Recognize state, errors prepended with '-'
                if tok[0] != '-':
                    self._index -= 1
                    break
                
                # Error state
                else:
                    self._handleError(tok, image, curChar)
                    return
            
            image.append(curChar)

        # Check to see if it is a keyword
        if "".join(image) in self._keywordTable:
            tok = "".join(image)
            
        self.curToken = tok
        self.curLexemme = "".join(image)        

# Test code, only ran when lex.py is ran separately
if __name__ == "__main__":
    lex = Lex()
    lex.readScanTable("../tables/DefaultScanTable.csv")
    lex.readTokenTable("../tables/DefaultTokenTable.csv")
    lex.readKeywordTable("../tables/DefaultKeywordTable.csv")
    lex.readSourceCode("../testFiles/DefaultTestFile.c")
        
    while not lex.eof(): 
        lex.getNextToken()
        if lex.curToken not in {"whiteSpace", "comment"}:
            print("Token: {:<12} Lexemme: {}".format(lex.curToken, \
                lex.curLexemme))