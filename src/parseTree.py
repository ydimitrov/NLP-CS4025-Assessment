def rec(line):
    # print line
    if len(line) == 1:
        return line[0].split(')')[0]
    # print line[0]
    if line[0][0] == '(':
        ans = rec(line[1:len(line)])
        # print ans
    else:
        ans = line[0].split(')')[0]
        # print ans
    dictionary = {}
    # print line[0].split('(')[1]
    dictionary[line[0].split('(')[1]] = ans
    # print dictionary
    return dictionary

def parseTree(s):
    s = [x.strip() for x in s.replace('\r\n', ' ').split(' ')
        if x]
    print s

    new_s =''
    for word in s:
        if word.startswith('('):
            new_s += '{"' + word[1:] + '": ['
        else:
            new_s += '"' + word.replace(')','') + '"' + ']}, ' * word.count(')')
    new_s = new_s[:-2].replace(', }', '}')
    print new_s
    bracketCount = 0
    tree = eval(new_s)
    return tree
