# DataFrameColumnCodeGenerator.ipynb

This python notebook defines a function that generates code to isolate individual columns of a pandas dataframe.
Each line generated contains the code for generating a variable from a column name as well as a comment that 
contains the column name for clarity. This will be helpful in the early stages of the project when we need to
isolate the columns that are helpful and the columns that aren't. It is much easier, at least for me, to organize 
over 300 columns of data when they are listed from top to bottom, rather than left to right, as they are in excel.

The function requires 3 inputs: the dataframe, a column position boolean, and an integer representing the number
of lines wanted in between each variable declaration.

The code must be run in a python notebook tool (e.g. jupyter notebook) with pandas and numpy installed in the 
environment. The notebook file must also be in the same directory as the data folder included.
