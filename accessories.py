#_______________________________________________________________________________
# Do all of the mail
def divide_chunks(l, n):
    for i in range(0, len(l), n): 
        yield l[i:i + n]
