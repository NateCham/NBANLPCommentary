import itertools

d_m = {
    1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31
}

def answer(x, y, z):
    count = 0
    ret_date = ''
    
    for p in itertools.permutations([x, y, z]):
        print(p)
        if is_date(p):
            count += 1
            ret_date = '%02d/%02d/%02d' % p
    
    if count > 1:
        return 'Ambiguous'
    else:
        return ret_date

def is_date(d_tup):
    return d_tup[0] <= 12 and d_tup[1] <= d_m[d_tup[0]]


if __name__ == '__main__':
    print(answer(19, 19, 3))
    print(answer(2, 30, 3))
