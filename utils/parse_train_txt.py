f = open('../datasets/train.txt')

d = dict()

for l in f.readlines():
    tmp = l.strip().split(' ')
    d[tmp[0]] = d.get(tmp[0], '') + ' %s,%s,%s,%s,%d' % (tmp[2], tmp[3], tmp[4], tmp[5], int(tmp[1])-1)

f.close()

f = open('../train.txt', 'w')

for k in d:
    f.write(k + d[k] + '\n')
