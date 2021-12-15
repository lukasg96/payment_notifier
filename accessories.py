# ______________________________________________________________________________
# Do all of the mail


def divide_chunks(mails, n):
    for i in range(0, len(mails), n):
        yield mails[i:i + n]
