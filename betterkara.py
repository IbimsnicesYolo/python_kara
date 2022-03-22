false = False
true = True
useless = kara

class betterkara:
#
    # Class Variables
    old_k = useless
    pickupleafs = 3
    debugactivated = false

    # 1 = remove leafs, 2 = put leafs, 3 = do nothing
    def pickupleaf(self, pickup):
        self.pickupleafs = pickup

    def getpickupmode(self):
        return self.pickupleafs

    # Bool debug activated
    def debugmode(self, mode):
        self.debugactivated = mode

    # Debug functions
    def debug(self, msg):
        tools.println(str(msg))
        if self.debugactivated:
            tools.showMessage(str(msg))
# enhancements
    # overwrite default functions
    def move_num(self, num):
        while num >= 1:
            if self.tree_f():
                break
            if self.mush_f():
                break
            if self.pickupleafs == 1:
                self.removeleaf()
            if self.pickupleafs == 2:
                self.putleaf()
            self.old_k.move()
            num -= 1

    def putleaf(self):
        if not self.old_k.onLeaf():
            self.old_k.putLeaf()

    def removeleaf(self):
        if self.old_k.onLeaf():
            self.old_k.removeLeaf()

    def turn_l(self, num):
        while num >= 1:
            self.old_k.turnLeft()
            num -= 1

    def turn_r(self, num):
        while num >= 1:
            self.old_k.turnRight()
            num -= 1

    def turn_180(self):
        self.turn_r(2)
#
    def tree_f(self):
        return self.old_k.treeFront()

    def tree_l(self):
        return self.old_k.treeLeft()

    def tree_r(self):
        return self.old_k.treeRight()

    def onleaf(self):
        return self.old_k.onLeaf()

    def mush_f(self):
        return self.old_k.mushroomFront()

    def getpos(self):
        return self.old_k.getPosition()
    def setpos(self, x, y):
        self.old_k.setPosition(x, y)

    # just if someone trys to use the old functions
    treeFront = tree_f
    treeLeft = tree_l
    treeRight = tree_r
    onLeaf = onleaf
    putLeaf = putleaf
    removeLeaf = removeleaf
    mushroomFront = mush_f
    getPosition = getpos
    setPosition = setpos

    def turnLeft(self):
        self.turn_l(1)
    def turnRight(self):
        self.turn_r(1)
    def move(self):
        self.move_num(1)
# look
    def islooking(self, dir):
        curr = self.getpos()
        curr.x += 1
        if world.getSizeX() < curr.x:
            curr.x = 0
        istree = false
        isleaf = false
        ismush = false
        if world.isLeaf(curr.x, curr.y):
            isleaf = true
            world.setLeaf(curr.x, curr.y, false)
        if world.isMushroom(curr.x, curr.y):
            ismush = true
            world.setMushroom(curr.x, curr.y, false)

        if world.isTree(curr.x, curr.y):
            istree = true
            world.setTree(curr.x, curr.y, false)

        world.setTree(curr.x, curr.y, true)
        a = false

        if dir == 0:
            a = self.tree_r()
        elif dir == 1:
            a = self.tree_f()
        elif dir == 2:
            a = self.tree_l()
        elif dir == 3:
            a = not self.tree_f() and not self.tree_l() and not self.tree_r()

        if not istree:
            world.setTree(curr.x, curr.y, false)
        if isleaf:
            world.setLeaf(curr.x, curr.y, true)
        if ismush:
            world.setMushroom(curr.x, curr.y, true)

        return a
# look 2
    # islooking* funcs are meant to check if kara is facing the specified direction currently
    def islookingup(self):
        return self.islooking(0)

    def islookingright(self):
        return self.islooking(1)

    def islookingdown(self):
        return self.islooking(2)

    def islookingleft(self):
        return self.islooking(3)

    # look* funcs are meant to force kara to turn to the given direction
    def lookdown(self):
        while not self.islookingdown():
            self.turn_l(1)

    def lookup(self):
        while not self.islookingup():
            self.turn_l(1)

    def lookleft(self):
        while not self.islookingleft():
            self.turn_l(1)

    def lookright(self):
        while not self.islookingright():
            self.turn_l(1)
# move_to
    # move func to move to specified coordinates
    def move_to(self, to_x, to_y):
        if to_x > world.getSizeX() - 1 or to_y > world.getSizeY() - 1:
            return

        curr = self.getpos()
        if curr.x != to_x:
            self.lookdown()
            if curr.x > to_x:
                self.turn_r(1)
                while self.getpos().x != to_x:
                    self.move()
            else:
                self.turn_l(1)
                while self.getpos().x != to_x:
                    self.move()
        if curr.y != to_y:
            turn_back = false
            self.lookdown()
            if curr.y > to_y:
                self.turn_180()
                turn_back = true
            while self.getpos().y != to_y:
                self.move()
            if turn_back:
                self.turn_180()
#
    length = {}
    length[" "] = 2
    symbols = {}
    symbols[" "] = []

    def edit(self):
        # creates field with specified size, let the user place sth and then read it and make a table for it
        # self.writestring(" 0123456789 \ 0123456789 \ 0123456789 \ \ \ \~~~~~~~~~~~") ### perfect Debug string
        output = ""

        def checkleaf():
            if self.onleaf():
                return ", [" + str(self.getpos().x - 1) + ", " + str(self.getpos().y - 1) + "]"
            return ""

        self.turn_l(1)
        output += checkleaf()
        while self.treeLeft():
            output += checkleaf()
            self.turn_r(1)
            for i in range(11):
                self.move()
                output += checkleaf()
            self.turn_180()
            self.move_num(11)
            self.turn_r(1)
            self.move()

        self.move_to(1, 1)
        self.lookdown()
        self.debug(output)
# writestring
    def writestring(self, string):
        string = string or ""
        l = len(string)
        margin_y = 3
        margin_x = 3
        y = 13
        x = 3
        biggest_x = 0

        def writesymbol(symbol):
            for i in range(len(self.symbols[symbol])):
                cords = self.symbols[symbol][i]
                self.move_to(cords[0] + margin_x, cords[1] + margin_y)
                self.putleaf()

        self.clear()
        if l == 0:
            self.move_to(0, 0)
            world.setSize(2, 2)
        else:
            self.move_to(0, 0)
            self.lookdown()
            for index in range(l):
                symbol = string[index]
                if not symbol:
                    continue
                if symbol == "\\":
                    x = 3
                    y += 10
                    margin_x = 3
                    margin_y += 10
                    self.move_to(x, y - 12)
                    world.setSize(biggest_x, y)
                    continue
                else:
                    x = x + self.length[symbol] + 3  # 3 spacing between letters
                    if x > 1000:  # line break
                        biggest_x = 1000
                        x = 3
                        y += 10
                        margin_x = 3
                        margin_y += 10
                    elif x > biggest_x:
                        biggest_x = x
                    world.setSize(biggest_x, y)
                writesymbol(symbol)
                margin_x += self.length[symbol] + 3  # 3 spacing between letters
        self.move_to(0, 0)
# clear, put
    def clear(self):
        x = world.getSizeX()
        y = world.getSizeY()
        self.move_to(0, 0)
        self.lookdown()
        curr_x = 0
        done = 0
        while done != 1:
            self.pickupleaf(1)
            while curr_x < x:
                self.move_num(y - 1)
                self.turn_l(1)
                self.move()
                self.turn_l(1)
                self.move_num(y - 1)
                self.turn_r(1)
                self.move()
                self.turn_r(1)
                curr_x += 2
            done = 1
        self.pickupleaf(3)
        self.move_to(0, 0)
        self.lookdown()

    def put(self):
        x = world.getSizeX()
        y = world.getSizeY()
        self.move_to(0, 0)
        self.lookdown()
        curr_x = 0
        done = 0
        while done != 1:
            self.pickupleaf(2)
            while curr_x < x:
                self.move_num(y - 1)
                self.turn_l(1)
                self.move()
                self.turn_l(1)
                self.move_num(y - 1)
                self.turn_r(1)
                self.move()
                self.turn_r(1)
                curr_x += 2
            done = 1
        self.pickupleaf(3)
        self.move_to(0, 0)
        self.lookdown()
#
    # Numbers
    length["0"] = 4
    length["1"] = 4
    length["2"] = 4
    length["3"] = 4
    length["4"] = 4
    length["5"] = 4
    length["6"] = 4
    length["7"] = 4
    length["8"] = 4
    length["9"] = 4
    symbols["0"] = [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [2, 6], [1, 6],
                    [0, 6], [0, 5], [0, 4], [0, 3], [0, 2], [0, 1]]
    symbols["1"] = [[0, 2], [1, 1], [2, 0], [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6]]
    symbols["2"] = [[0, 1], [1, 0], [2, 0], [3, 1], [3, 2], [2, 3], [1, 4], [0, 5], [0, 6], [1, 6], [2, 6], [3, 6]]
    symbols["3"] = [[0, 0], [1, 0], [2, 0], [3, 1], [3, 2], [2, 3], [1, 3], [0, 3], [3, 4], [3, 5], [2, 6], [1, 6],
                    [0, 6]]
    symbols["4"] = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 3], [2, 3], [3, 3], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5],
                    [2, 6]]
    symbols["5"] = [[3, 0], [2, 0], [1, 0], [0, 0], [0, 1], [0, 2], [0, 3], [1, 3], [2, 3], [3, 4], [3, 5], [2, 6],
                    [1, 6], [0, 6]]
    symbols["6"] = [[3, 0], [2, 0], [1, 0], [0, 0], [0, 1], [0, 2], [0, 3], [1, 3], [2, 3], [3, 3], [3, 4], [3, 5],
                    [3, 6], [2, 6], [1, 6], [0, 6], [0, 5], [0, 4]]
    symbols["7"] = [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1], [2, 2], [0, 3], [1, 3], [2, 3], [3, 3], [1, 4], [0, 5],
                    [0, 6]]
    symbols["8"] = [[2, 0], [3, 1], [3, 2], [2, 3], [3, 4], [3, 5], [2, 6], [1, 6], [0, 5], [0, 4], [1, 3], [0, 2],
                    [0, 1], [1, 0]]
    symbols["9"] = [[0, 6], [1, 6], [2, 6], [3, 6], [3, 5], [3, 4], [3, 3], [3, 2], [3, 1], [3, 0], [2, 0], [1, 0],
                    [0, 0], [0, 1], [0, 2], [0, 3], [1, 3], [2, 3]]

    # more
    symbols["!"] = [[1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 6]]
    length["!"] = 3
    symbols["+"] = [[1, 2], [1, 3], [2, 3], [0, 3], [1, 4]]
    length["+"] = 3
    symbols["-"] = [[0, 3], [1, 3], [2, 3], [3, 3]]
    length["-"] = 4
    symbols["~"] = [[0, 3], [1, 2], [2, 3], [3, 4], [4, 3]]
    length["~"] = 5
    symbols["="] = [[0, 2], [1, 2], [2, 2], [3, 2], [0, 4], [1, 4], [2, 4], [3, 4]]
    length["="] = 4
    symbols["*"] = [[0, 2], [1, 3], [2, 2], [2, 4], [0, 4]]
    length["*"] = 3
    symbols["?"] = [[0, 1], [1, 0], [2, 0], [3, 1], [3, 2], [2, 3], [1, 3], [1, 4], [1, 6]]
    length["?"] = 4
    symbols["^"] = [[0, 2], [1, 1], [2, 0], [3, 1], [4, 2]]
    length["^"] = 5
    symbols['"'] = [[0, 0], [0, 1], [0, 2], [2, 2], [2, 1], [2, 0]]
    length['"'] = 3
    symbols["'"] = [[1, 0], [1, 1], [1, 2]]
    length["'"] = 3
    symbols["#"] = [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [3, 5], [3, 4], [3, 3], [3, 2], [3, 1], [4, 2], [4, 4],
                    [2, 2], [2, 4], [0, 2], [0, 4]]
    length["#"] = 5

    # letters
    length["a"] = 5
    symbols["a"] = [[0, 4], [0, 5], [1, 1], [1, 3], [1, 6], [2, 1], [2, 3], [2, 6], [3, 1], [3, 3], [3, 5], [4, 2],
                    [4, 3], [4, 4], [4, 5], [4, 6]]
    length["b"] = 4
    symbols["b"] = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 3], [1, 6], [2, 3], [2, 6], [3, 4], [3, 5]]
    length["c"] = 3
    symbols["c"] = [[0, 4], [0, 5], [1, 3], [1, 6], [2, 3], [2, 6]]
    length["d"] = 4
    symbols["d"] = [[0, 4], [0, 5], [1, 3], [1, 6], [2, 3], [2, 6], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6]]
    length["e"] = 4
    symbols["e"] = [[0, 3], [0, 4], [0, 5], [1, 2], [1, 4], [1, 6], [2, 2], [2, 4], [2, 6], [3, 3], [3, 4], [3, 6]]
    length["f"] = 4
    symbols["f"] = [[0, 3], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [2, 0], [2, 3], [3, 0], [3, 3]]
    length["g"] = 4
    symbols["g"] = [[0, 4], [0, 5], [1, 3], [1, 6], [1, 9], [2, 3], [2, 6], [2, 9], [3, 3], [3, 4], [3, 5], [3, 6],
                    [3, 7], [3, 8]]
    length["h"] = 4
    symbols["h"] = [[0, 0], [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 3], [2, 3], [3, 4], [3, 5],
                    [3, 6]]
    length["i"] = 3
    symbols["i"] = [[1, 1], [1, 3], [1, 4], [1, 5], [1, 6]]
    length["j"] = 5
    symbols["j"] = [[0, 8], [1, 9], [2, 5], [2, 9], [3, 2], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8], [4, 5]]
    length["k"] = 4
    symbols["k"] = [[0, 0], [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 4], [2, 3], [2, 5], [3, 2],
                    [3, 6]]
    length["l"] = 4
    symbols["l"] = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 6], [2, 6], [3, 5]]
    length["m"] = 5
    symbols["m"] = [[0, 4], [0, 5], [0, 6], [1, 3], [2, 4], [2, 5], [2, 6], [3, 3], [4, 4], [4, 5], [4, 6]]
    length["n"] = 4
    symbols["n"] = [[0, 3], [0, 4], [0, 5], [0, 6], [1, 3], [2, 3], [3, 4], [3, 5], [3, 6]]
    length["o"] = 4
    symbols["o"] = [[0, 4], [0, 5], [1, 3], [1, 6], [2, 3], [2, 6], [3, 4], [3, 5]]
    length["p"] = 4
    symbols["p"] = [[0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [1, 3], [1, 6], [2, 3], [2, 6], [3, 4], [3, 5]]
    length["q"] = 4
    symbols["q"] = [[0, 4], [0, 5], [1, 3], [1, 6], [2, 3], [2, 6], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8]]
    length["r"] = 4
    symbols["r"] = [[0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 3], [2, 2], [3, 2]]
    length["s"] = 4
    symbols["s"] = [[0, 3], [0, 6], [1, 2], [1, 4], [1, 6], [2, 2], [2, 4], [2, 6], [3, 2], [3, 5]]
    length["t"] = 4
    symbols["t"] = [[0, 2], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [2, 2], [2, 6], [3, 6]]
    length["u"] = 4
    symbols["u"] = [[0, 3], [0, 4], [0, 5], [1, 6], [2, 6], [3, 3], [3, 4], [3, 5]]
    length["v"] = 5
    symbols["v"] = [[0, 4], [1, 5], [2, 6], [3, 5], [4, 4]]
    length["w"] = 5
    symbols["w"] = [[0, 4], [0, 5], [1, 6], [2, 4], [2, 5], [3, 6], [4, 4], [4, 5]]
    length["x"] = 4
    symbols["x"] = [[0, 3], [0, 6], [1, 4], [1, 5], [2, 4], [2, 5], [3, 3], [3, 6]]
    length["y"] = 5
    symbols["y"] = [[0, 9], [1, 4], [1, 5], [1, 8], [2, 6], [2, 7], [3, 6], [4, 4], [4, 5]]
    length["z"] = 4
    symbols["z"] = [[0, 3], [0, 6], [1, 3], [1, 5], [1, 6], [2, 3], [2, 4], [2, 6], [3, 3], [3, 6]]

kara = betterkara()