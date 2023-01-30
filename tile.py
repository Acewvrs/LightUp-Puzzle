import wx

class Tile(wx.Button):
    # constants for tile_state 
    BLOCK = 0
    DIM = 1
    LIT = 2
    
    def __init__(self, parent, tile_state=DIM, adj_bulbs=-1, x=-1, y=-1, **k):
        wx.Button.__init__(self, parent=parent, **k)
        # tile_state=DIM, adj_bulbs=-1,
        self.x = y
        self.y = x
        # self.SetSize((TILE_SIZE, TILE_SIZE))
        self.parent = parent #reference to board panel
        self.board = parent.board
        self.state = tile_state
        self.number = adj_bulbs #number on the (black) tile indicating the number of adjacent bulbs
        self.light_bulb = False
        self.light_bulb_img = parent.light_bulb_img
        self.red_X_img = parent.red_X_img
        self.light_board = parent.light_board # board to keep track of how many light bulbs are lighting a tile
        self.enabled = True

        # -------------------------------------------
        # event functions
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        # self.Bind(wx.EVT_ENTER_WINDOW, self.OnHover)

        if (self.state == self.BLOCK):
            self.SetBackgroundColour('black')
            self.Disable()
    
    # def OnHover(self, event):
    #     if (self.state == self.DIM):
    #         self.SetBackgroundColour('white')
    #     elif (self.state == self.LIT):
    #         self.SetBackgroundColour('yellow')

    def OnLeftClick(self, event):
        # LEFT CLICK: place or remove lightbulbs
        # you can click on a tile in two cases: to light up a tile or remove light bulb
        if (self.state == self.DIM and self.enabled):
            self.light_bulb = True
            self.showLightBulb()
            self.lightOn()
            self.lightAll()

        elif (self.light_bulb == True and self.enabled):    
            self.light_bulb = False
            self.removeImg()
            self.lightOff()
            self.lightOffAll()
        
    def OnRightClick(self, event):
        # RIGHT CLICK: soft lock tiles to indicate bulbs can't be here
        if (self.enabled and not self.light_bulb):
            self.enabled = False
            self.showRedX()
        elif (not self.enabled and not self.light_bulb):
            self.enabled = True
            self.removeImg()

    def showLightBulb(self):
        self.SetBitmap(self.light_bulb_img)
        self.Layout()
        self.Update()
    
    def removeImg(self):
        # remove any lightbulb or red X bitmap on tile
        self.SetBitmap(wx.NullBitmap)
        self.Layout()
        self.Update()
    
    def showRedX(self):
        self.SetBitmap(self.red_X_img)
        self.Layout()

    def lightAll(self):
        # light up all tiles in the same row/col
        # update the info on board as you determine which tiles will light up
        for i in range(self.y, len(self.board)):
            if (self.board[self.x][i].getState() == self.BLOCK):
                break
            self.board[self.x][i].lightOn()
            self.light_board[self.x][i] += 1
        
        for i in range(self.y, -1, -1):
            if (self.board[self.x][i].getState() == self.BLOCK):
                break
            self.board[self.x][i].lightOn()
            self.light_board[self.x][i] += 1

        for i in range(self.x, len(self.board)):
            if (self.board[i][self.y].getState() == self.BLOCK):
                break
            self.board[i][self.y].lightOn() 
            self.light_board[i][self.y] += 1

        for i in range(self.x, -1, -1):
            if (self.board[i][self.y].getState() == self.BLOCK):
                break
            self.board[i][self.y].lightOn() 
            self.light_board[i][self.y] += 1
        

    def lightOn(self):
        if (self.state == self.DIM):
            self.state = self.LIT
            self.SetBackgroundColour("yellow")

    def lightOffAll(self):
        # light off all tiles in the same row/col
        for i in range(self.y, len(self.board)):
            if (self.board[self.x][i].getState() == self.BLOCK):
                break

            self.light_board[self.x][i] -= 1
            if (self.light_board[self.x][i] == 0):
                self.board[self.x][i].lightOff()
            
        
        for i in range(self.y, -1, -1):
            if (self.board[self.x][i].getState() == self.BLOCK):
                break

            self.light_board[self.x][i] -= 1
            if (self.light_board[self.x][i] == 0):
                self.board[self.x][i].lightOff()

        for i in range(self.x, len(self.board)):
            if (self.board[i][self.y].getState() == self.BLOCK):
                break

            self.light_board[i][self.y] -= 1
            if (self.light_board[i][self.y] == 0):
                self.board[i][self.y].lightOff() 

        for i in range(self.x, -1, -1):
            if (self.board[i][self.y].getState() == self.BLOCK):
                break

            self.light_board[i][self.y] -= 1
            if (self.light_board[i][self.y] == 0):
                self.board[i][self.y].lightOff() 

    def lightOff(self):
        if (self.state == self.LIT):
            self.state = self.DIM
            self.SetBackgroundColour('white')
    
    def getState(self):
        return self.state
    
    def getNum(self):
        return self.number

    def hasLightBulb(self):
        return self.light_bulb
