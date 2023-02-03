import unittest
import lex
import gui

class LexTester(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.lex = lex.Lex()
        self.lex.readScanTable("../" + gui.GUI.DEF_SCAN)
        self.lex.readTokenTable("../" + gui.GUI.DEF_TOKEN)
        self.lex.readKeywordTable("../" + gui.GUI.DEF_KEY)
        
        
        
    def testInt(self):
        self.lex.setSourceCode("3 0234 0xAfe7261")
        
        self.lex.getNextToken()
        self.assertEqual(self.lex.curToken, "intLiteral", "Expected int")
        self.assertEqual(self.lex.curLexemme, "3", "Expected 3")
        
        self.lex.getNextToken()
        self.lex.getNextToken()
        self.assertEqual(self.lex.curToken, "intLiteral", "Expected int")
        self.assertEqual(self.lex.curLexemme, "0234", "Expected 0234")
        
        self.lex.getNextToken()
        self.lex.getNextToken()
        self.assertEqual(self.lex.curToken, "intLiteral", "Expected int")
        self.assertEqual(self.lex.curLexemme, "0xAfe7261", "Expected 0xAfe7261")
        
        
        
    def testFloat(self):
        self.lex.setSourceCode("1. .432e+000010 0012.")
                
        self.lex.getNextToken()
        self.assertEqual(self.lex.curToken, "floatLiteral", "Expected float")
        self.assertEqual(self.lex.curLexemme, "1.", "Expected 1.")

        self.lex.getNextToken()
        self.lex.getNextToken()
        self.assertEqual(self.lex.curToken, "floatLiteral", "Expected float")
        self.assertEqual(self.lex.curLexemme, ".432e+000010", "Expected .432e+000010")
        
        self.lex.getNextToken()
        self.lex.getNextToken()
        self.assertEqual(self.lex.curToken, "floatLiteral", "Expected float")
        self.assertEqual(self.lex.curLexemme, "0012.", "Expected 0012.")
        
        
    
    def testErrors(self):
        self.lex.setSourceCode("03248231 # \b 12.0e .9E-")
        
        self.lex.getNextToken()
        self.assertEqual(self.lex.errorFlag, True, "Error flag should be True")
        self.assertEqual(self.lex.errorMessage, "-Illegal octal number: 03248231", "Expected illegal octal number")
        
        self.lex.getNextToken()
        self.assertEqual(self.lex.errorFlag, True, "Error flag should be True")
        self.assertEqual(self.lex.errorMessage, "-Illegal character or backslash out of char or string: #", "Expected illegal character or backslash out of char or string")
        
        self.lex.getNextToken()
        self.lex.getNextToken()
        print(self.lex.curLexemme, self.lex.curToken)
        self.assertEqual(self.lex.errorFlag, True, "Error flag should be True")
        self.assertEqual(self.lex.errorMessage, "-Illegal character or backslash out of char or string: \\", "Expected illegal character or backslash out of char or string")
        
        self.lex.getNextToken()
        self.lex.getNextToken()
        self.assertEqual(self.lex.errorFlag, True, "Error flag should be True")
        self.assertEqual(self.lex.errorMessage, "-Exponation char {e | E} must be followed by {+ | - | 0-9}: 12.0e", "Expected illegal exponation")
        
        self.lex.getNextToken()
        self.lex.getNextToken()
        self.assertEqual(self.lex.errorFlag, True, "Error flag should be True")
        self.assertEqual(self.lex.errorMessage, "-Illegal exponation; {e | E}{+ | -} must be followed by {0-9}: .9E-", "Expected illegal exponation")

unittest.main()