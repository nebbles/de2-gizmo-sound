# test file

# Open data file
infile = open("example.txt", "r") # "r" is for read

# Initialise empty lists
tune = []

# Loop through infile and write to x and y lists
with open("example.txt", "r") as f:
    content = f.readlines()

# Close the filehandle
infile.close()
f.close()

print tune
print content
