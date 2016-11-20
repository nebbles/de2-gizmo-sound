# test file

## -- IMPORT TUNE FROM FILE -- ##
infile = open("example.txt", "r") # Open data file -- "r" is for read
tune = [line.rstrip('\n') for line in infile]
infile.close() # Close the filehandle

print tune
print lines
print lines[4][0]
print lines[4][1]
print lines[4][2]
