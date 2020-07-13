import csv
import sys
class CommonModulusAttack:
    def __init__(self, c1, c2, e1, e2, N):
        self.c1 = c1
        self.c2 = c2
        self.e1 = e1
        self.e2 = e2
        self.N = N
    
    def xgcd(self,a,b):
        if b == 0:
            return [1,0,a]
        else:
            x,y,d = self.xgcd(b, a%b)
            return [y, x - (a//b)*y, d]

    def gcd(self,a, b):
        while a != 0:
            a, b = b % a, a
        return b

    def moduloInverse(self,a, m):
        if self.gcd(a, m) != 1:
            return None
        x1, x2, x3 = 1, 0, a
        y1, y2, y3 = 0, 1, m
        while y3 != 0:
            q = x3 // y3
            y1, y2, y3, x1, x2, x3 = (x1 - q * y1), (x2 - q * y2), (x3 - q * y3), y1, y2, y3
        return x1 % m

def main():
    with open('./crackme.csv') as f:
        reader = csv.reader(f)
        data = list(reader)
    cma = CommonModulusAttack(int(data[0][1],16),int(data[1][1],16),int(data[2][1],16),int(data[3][1],16),int(data[4][1],16))
    euclidians=cma.xgcd(cma.e1,cma.e2)
    a=euclidians[0]	
    b=euclidians[1]
    eq1=cma.moduloInverse(cma.c2,cma.N)
    #(c1^a * eq1^-b) mod N
    result= pow(eq1,-b,cma.N) * pow(cma.c1,a,cma.N)
    finalhex=hex(result%(cma.N))
    print(''.join([chr(int(''.join(c), 16)) for c in zip(finalhex[2::2],finalhex[3::2])]))

if __name__ == "__main__":
    main()
        