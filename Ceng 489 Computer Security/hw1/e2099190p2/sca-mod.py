import sys
class SideChannel:
    def __init__(self,cipher,N,d=None,start=0,jump=25,bound = 5,M=None):
        self.cipher = cipher
        self.N = N
        self.d = d
        self.start = start
        self.jump = jump
        self.bound = bound
        self.M = M
    
    def set_d(self,d):
        self.d = d

    def set_M(self,M):
        self.M = M

def main():
    cipher = sys.stdin.readline()
    N = sys.stdin.readline()
    # with open('./ptrace_input.txt') as inputfile:
    #     cipherandN = inputfile.read().split("\n")
    with open('./ptrace.trc') as tracefile:
        powertracedata = tracefile.read().split("\n")
    sca = SideChannel(int(cipher[:-1],16),int(N,16))
    binaryarray = []
    operationarray = [] # 1 -> sq+mult, 0-> sq
    length = len(powertracedata)

    if len(powertracedata[-1].strip()) == 0:
        length = length -1

    for point_index in range(sca.start, length, sca.jump):
        if float(powertracedata[point_index]) > sca.bound:
            binaryarray.append(1)
        else:
            binaryarray.append(0)

    sqMult = 0
    for value in binaryarray:
        if value:
            sqMult+=1
        else:
            if sqMult == 5:
                operationarray.append(1)
            elif sqMult == 3:
                operationarray.append(0)
            sqMult = 0
    sca.set_d(int("".join(str(x) for x in operationarray)[::],2))
    sca.set_M(hex(pow(sca.cipher, sca.d, sca.N)))
    print(''.join([chr(int(''.join(c), 16)) for c in zip(sca.M[2::2],sca.M[3::2])]))
if __name__ == "__main__":
    main()