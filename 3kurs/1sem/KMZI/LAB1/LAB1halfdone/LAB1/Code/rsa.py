from math import gcd
# Ввод
#     digit - число, тотиент Эйлера которого нужно найти
# Вывод
#     тотиент Эйлера
def IsPrime(n):
    d = 2
    while d * d <= n and n % d != 0:
        d += 1
    return d * d > n

def eulers_totient(digit):
    counter = 0
    for i in range(1, digit + 1):
        if gcd(digit, i) == 1:
            counter += 1
    return counter

def RSAopenCloseKey(p=7,q=13):
    if(not IsPrime(p) or not IsPrime(q)): return ValueError
    n=p*q
    elier = (p-1)*(q-1)
    e=1
    for i in range(2,elier):
        if gcd(i,elier) == 1:
            e = i
            break
    openkey = (e,n)
    d = 0
    while True:
        if ((d*elier+1)/e) % 1 == 0: break
        else: d+=1
    closekey= (d,n)
    return openkey,closekey