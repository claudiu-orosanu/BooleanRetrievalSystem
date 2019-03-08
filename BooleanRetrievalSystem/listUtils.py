def intersect_lists(l1, l2):
    result = []
    i, j, k = 0, 0, 0

    while i < len(l1) and j < len(l2):
        if l1[i] == l2[j]:
            result.append(l1[i])
            i += 1
            j += 1
        elif l1[i] < l2[j]:
            i += 1
        else:
            j += 1

    return result


def union_lists(l1, l2):
    result = []
    i, j = 0, 0

    while i < len(l1) and j < len(l2):
        if l1[i] == l2[j]:
            result.append(l1[i])
            i += 1
            j += 1
        elif l1[i] < l2[j]:
            result.append(l1[i])
            i += 1
        else:
            result.append(l2[j])
            j += 1

    while i < len(l1):
        result.append(l1[i])
        i += 1

    while j < len(l2):
        result.append(l2[j])
        j += 1

    return result