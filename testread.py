# test file

# Open data file
infile = open("example.txt", "r") # "r" is for read

# Initialise empty lists
tune = []

# Loop through infile and write to x and y lists
for line in infile:
    tune.append(str(line))

# Close the filehandle
infile.close()

print tune
