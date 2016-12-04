# test file

## -- IMPORT TUNE FROM FILE -- ##
infile = open("example.txt", "r") # Open data file -- "r" is for read
tune = [line.rstrip('\n') for line in infile]
infile.close() # Close the filehandle

print tune
print tune[4][0]
print tune[4][1]
print tune[4][2]

print len(tune)
