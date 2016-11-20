# test file

# Open data file
infile = open("example.txt", "r") # "r" is for read
lines = [line.rstrip('\n') for line in infile]

# Initialise empty lists
tune = []

# Loop through infile and write to x and y lists


# Close the filehandle
infile.close()

print tune
print lines
print lines[4][0]
print lines[4][1]
print lines[4][2]
