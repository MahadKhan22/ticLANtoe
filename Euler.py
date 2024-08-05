import sys

class Node:
    def __init__(self, val, trueLeaf=False):
        self.left = None
        self.right = None
        self.val = val
        self.trueLeaf = trueLeaf

    def isDed(self):
        if self.trueLeaf:
            return False



    def __str__(self):
        return(f"{self.left}  {self.val}  {self.right}")

def main():
    global flag

    flag = True
    createPopulate()
    for i in range(2):
        print(pathfind())
    pathfind()
    for i in range(75,110):
        print(tree[i])

def createPopulate():
    global tree

    def triangle(set):
        sum=0
        while set != 1:
            sum += set
            set -= 1
        return (sum)

    tree = [None]*120

    def fill():
        tree[0] = Node(75)
        tree[1] = Node(95)
        tree[2] = Node(64)
        tree[3] = Node(17)
        tree[4] = Node(47)
        tree[5] = Node(82)
        tree[6] = Node(18)
        tree[7] = Node(35)
        tree[8] = Node(87)
        tree[9] = Node(10)
        tree[10] = Node(20)
        tree[11] = Node(4)
        tree[12] = Node(82)
        tree[13] = Node(47)
        tree[14] = Node(65)
        tree[15] = Node(19)
        tree[16] = Node(1)
        tree[17] = Node(23)
        tree[18] = Node(75)
        tree[19] = Node(3)
        tree[20] = Node(34)
        tree[21] = Node(88)
        tree[22] =  Node(2)
        tree[23] = Node(77)
        tree[24] = Node(73)
        tree[25] = Node(7)
        tree[26] = Node(63)
        tree[27] = Node(67)
        tree[28] = Node(99)
        tree[29] = Node(65)
        tree[30] = Node(4)
        tree[31] = Node(28)
        tree[32] = Node(6)
        tree[33] = Node(16)
        tree[34] = Node(70)
        tree[35] = Node(92)
        tree[36] = Node(41)
        tree[37] = Node(41)
        tree[38] = Node(26)
        tree[39] = Node(56)
        tree[40] = Node(83)
        tree[41] = Node(40)
        tree[42] = Node(80)
        tree[43] = Node(70)
        tree[44] = Node(33)
        tree[45] = Node(41)
        tree[46] = Node(48)
        tree[47] = Node(72)
        tree[48] = Node(33)
        tree[49] = Node(47)
        tree[50] = Node(32)
        tree[51] = Node(37)
        tree[52] = Node(16)
        tree[53] = Node(94)
        tree[54] = Node(29)
        tree[55] = Node(53)
        tree[56] = Node(71)
        tree[57] = Node(44)
        tree[58] = Node(65)
        tree[59] = Node(25)
        tree[60] = Node(43)
        tree[61] = Node(91)
        tree[62] = Node(52)
        tree[63] = Node(97)
        tree[64] = Node(51)
        tree[65] = Node(14)
        tree[66] = Node(70)
        tree[67] = Node(11)
        tree[68] = Node(33)
        tree[69] = Node(28)
        tree[70] = Node(77)
        tree[71] = Node(73)
        tree[72] = Node(17)
        tree[73] = Node(78)
        tree[74] = Node(39)
        tree[75] = Node(68)
        tree[76] = Node(17)
        tree[77] = Node(57)
        tree[78] = Node(91)
        tree[79] = Node(71)
        tree[80] = Node(52)
        tree[81] = Node(38)
        tree[82] = Node(17)
        tree[83] = Node(14)
        tree[84] = Node(91)
        tree[85] = Node(43)
        tree[86] = Node(58)
        tree[87] = Node(50)
        tree[88] = Node(27)
        tree[89] = Node(29)
        tree[90] = Node(48)
        tree[91] = Node(63)
        tree[92] = Node(66)
        tree[93] = Node(4)
        tree[94] = Node(68)
        tree[95] = Node(89)
        tree[96] = Node(53)
        tree[97] = Node(67)
        tree[98] = Node(30)
        tree[99] = Node(73)
        tree[100] = Node(16)
        tree[101] = Node(69)
        tree[102] = Node(87)
        tree[103] = Node(40)
        tree[104] = Node(31)
        tree[105] = Node(4, True)
        tree[106] = Node(62, True)
        tree[107] = Node(98, True)
        tree[108] = Node(27, True)
        tree[109] = Node(23, True)
        tree[110] = Node(9, True)
        tree[111] = Node(70, True)
        tree[112] = Node(98, True)
        tree[113] = Node(73, True)
        tree[114] = Node(93, True)
        tree[115] = Node(38, True)
        tree[116] = Node(53, True)
        tree[117] = Node(60, True)
        tree[118] = Node(4, True)
        tree[119] = Node(23, True) 
    fill()

    set = 1
    c=1
    i = 0
    while c < 119:
        tree[i].left = c
        tree[i].right = c+1

        if triangle(set) == i:
            set += 1
            c += 1
        c += 1
        i += 1

def pathfind(): # find leftmost possible path. once reached leaf, kill leaf so next iter wont go down same path, returns sum of path

    done = False
    thisNode = tree[0]

    while not done:
        sum += thisNode.val
        prevNode = thisNode

        if not tree[thisNode.left].isDed():
            dir = "left"
            if flag:
                print("{dir} at {thisNode.val}")
            thisNode = tree[thisNode.left]

        elif not tree[thisNode.right].isDed():
            dir = "right"
            if flag:
                print("{dir} at {thisNode.right}")
            if not prevNode.left:
                prevNode.right = None
            else:
                prevNode.left = None

            thisNode = tree[thisNode.left]
    

        if thisNode.trueLeaf:
            sum += thisNode.val
            done = True
            



main()
    
'''
    sum = 0
    thisNode = tree[0]
    sum += thisNode.val
    while not thisNode.isLeaf():

        prevNode = thisNode
        if thisNode.left != None and not thisNode.isDedEnd():
            if flag:
                print(f"left at {thisNode.val}")
            thisNode = tree[thisNode.left]
            dir = "left"

        elif not thisNode.isDedEnd():
            if flag:
                print(f"right on {thisNode.val}")
            thisNode = tree[thisNode.right]
            dir = "right"

        else:
            sys.exit("error1")
        sum += thisNode.val
    if dir == "left":
        prevNode.left = None
    else:
        prevNode.right = None
    return sum
'''