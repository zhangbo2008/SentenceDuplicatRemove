import distance

def edit_distance(s1, s2):
    return distance.levenshtein(s1, s2)

tmp=edit_distance("���ƺ�Ӧ����","���ƺ�")

print(tmp)

