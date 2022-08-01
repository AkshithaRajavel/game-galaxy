for _ in range(int(input())):
    n,k = map(int,input().split())
    A = input()
    if (A == '0'*n) | (A == '1'*n):
        print(k - 1)
        continue
    i,m = A.find('1'),0
    ind = i
    s = A*2
    while i < n:
        a = s.find('0',i)
        if a - i > m:
            m = a-i
            ind = i
        a = s.find('1',a)
        i = a
    B = A[ind:] + A[:ind]
    print(B)
    s = B*2
    a =s.find(B,1)
    r = ind + (int(a/n)*n + a%n)*(k-1)
    print(r)
    print('\n')