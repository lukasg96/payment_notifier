
def divide_rest(mails, n):
    list = []
    for i in range(0, len(mails), n):
        list.append(mails[i:i + n])
    return list

def divide_chunks(mails, n0, n):
    list = [mails[:n0]] + divide_rest(mails[n0:], n)
    return list
