# +----------------------------------------------------------------------------
#
# Name:     Brandon Mitchell
# Description:  The entry point for the lexical analyzer.  Being a *.pyw, no 
#               command window should open.
#
# +----------------------------------------------------------------------------

from source.lex import Lex
from source.gui import GUI, missingFilesError

# +----------------------------------------------------------------------------

def main():
    lex = Lex()

    # Don't let program run if we are missing the default files
    if not all([lex.readScanTable(GUI.DEF_SCAN), \
        lex.readTokenTable(GUI.DEF_TOKEN), \
        lex.readKeywordTable(GUI.DEF_KEY), \
        lex.readSourceCode(GUI.DEF_SOURCE)]):
        
        missingFilesError()
        return
    
    # Pass the lex into the GUI and run!  I believe the big word for this is 
    # "depedency injection".
    gui = GUI(lex)
    gui.mainloop()

if __name__ == "__main__":
    main()