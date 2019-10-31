import distance

def edit_distance(s1, s2):
    return distance.levenshtein(s1, s2)

tmp=edit_distance("鼠标称呼应该是","鼠标称呼")

print(tmp)

