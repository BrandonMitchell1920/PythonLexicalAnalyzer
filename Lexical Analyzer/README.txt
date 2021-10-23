"tkinter" is used for GUI elements.  It should be installed by default.

To run, double click "main.pyw" or right-click and hit "open" or simply call on 
the command line.  The "*.pyw" extension means no command window will be opened 
when ran as it isn't needed with the GUI.

The analyzer will open default tables and a source code file at default 
locations.  These files must be present or the program will not start-up. The 
GUI sets the default locations for these files, so you can change them there.
There are various other files availabe to test the table and my DFA.  There is
also a file with several errors in it to test each error state.

Several options are available via buttons in the window, but there are other
options in the menu bar.  For example, you can restart scanning or save the 
output.  "Next Token" retrieves the next token and "Auto Scan" retrieves all
the tokens.

+------------------------------------------------------------------------------

I put error messages in to the token table at each dead state.  That way, I can
give more accurate error info by just printing out the token.  Since I know
what led to that state, it is a lot more helpful.  Still, it can be a bit 
unclear sometimes.  For a lexical analyzer used in a compiler, having some part 
parse the image and give a more detailed message from there would probably
help.  For example '' and '12' and ' will all say that a char must end with a 
single quote.  They will show '' and '12 and ' for the image.  It may be just
a bit unclear what was the exact problem as these are three different errors 
with the same state.  Empty char, char with too many characters, rouge ' at the
end of line.  Creating extra states just to handle the various different error
states could be done.  Get a ' followed by ', go to this state to error out,
etc.

In addition, I don't print out line or column numbers as I read the file in as 
a big ol' string.  However, each row is seperated by a newline, so it would not 
be difficult to figure out what row and column the error is in.  I will likely
include that in my C# analyzer.  I don't want to make it a 2D matrix as that 
complicates some things.

+------------------------------------------------------------------------------

The lexical analyzer and GUI are seperated.  I figured this would make the 
translation process easier since the GUI stuff is going to be different in each 
language where the lexical analyer will just be a straight translation.  This
also makes reusing the lexical analyer much easier should I want to put it into
another project.

+------------------------------------------------------------------------------

Also, I put the spooky pumpkin witch as the program's icon!  Spooky!