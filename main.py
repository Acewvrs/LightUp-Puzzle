import wx
# import light_up as lu
import random

SMALL_SIZE = 7
MEDIUM_SIZE = 10
LARGE_SIZE = 14

def load_and_resize_bmp(fn, w, h):
    '''A helper function that loads and resizes and image, returning a wx.Bitmap object'''

    # Load wx.Bitmap from fn
    bmp = wx.Bitmap(fn)
    
    # Convert wx.Bitmap to wx.Image
    img = bmp.ConvertToImage()

    # Use wx.Image method to scale the image based on w and h
    img = img.Scale(int(w), int(h), wx.IMAGE_QUALITY_HIGH)

    # Convert wx.Image back to wx.Bitmap and return to caller
    bmp = img.ConvertToBitmap()    
    return bmp

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

        # if (tile_state == 2):
        #     self.showLightBulb()
        
        # self.SetLabel(str(int(x)) + ' ' + str(int(y)))

        # -------------------------------------------
        # event functions
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        # self.Bind(wx.EVT_ENTER_WINDOW, self.OnHover)
    
        # self.SetLabel(str(x) + ' ' + str(y))
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

    def setNum(self, num):
        self.number = num
        self.SetLabel = self.number

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Light UP Generator', style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER, size=(APP_WIDTH, APP_HEIGHT))
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # main_panel = Info(self)
        self.initpos = 600

        self.sp = wx.SplitterWindow(self)
        self.board = Board(self.sp, self)
        self.board.SetBackgroundColour("white")

        self.info = Info(self.sp, self)
        # self.info.SetBackgroundColour("sky blue")

        self.sp.SplitVertically(self.board, self.info, self.initpos)
        self.sp.SetMinimumPaneSize(100)

        # main_sizer.Add(main_panel)
        
        # self.SetSizer(main_sizer)
        # self.Fit()   
        
        # self.board.Start()

        self.CenterOnScreen(wx.BOTH)
        self.Show()


class Board(wx.Panel):
    UND = -1
    BLOCK = 0
    LIGHT_BULB = 1
    
    def __init__(self, parent, MainFrame):
        wx.Panel.__init__(self, parent)
        #------------
        self.main_frame = MainFrame

        # Delete flickers.
        if wx.Platform == "__WXMSW__":
            self.SetDoubleBuffered(True)

        # -------------------
        # Load images (bitmap)
        bulb_img_scale = 0.7
        X_img_scale = 0.4
        self.light_bulb_img = load_and_resize_bmp("assets\light_bulb.png", TILE_SIZE * bulb_img_scale, TILE_SIZE * bulb_img_scale)
        self.red_X_img = load_and_resize_bmp("assets\\red_x.png", TILE_SIZE * X_img_scale, TILE_SIZE * X_img_scale)
        # self.light_bulb_img = wx.StaticBitmap(self, bitmap=self.light_bulb)
        
        # -----------------------
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.grid = wx.BoxSizer(wx.VERTICAL)
        self.board = []
        self.board_data = []        # solution represented as data where 0: blocks, 1: empty, 2: lightbulb
        self.light_board = []       # keeps track of how many lightbulbs are lighting each tile
        self.available_tiles = []   # list of (x,y) where lightbulbs can be placed
        self.block_pos = []         # list of (x,y) of blocks
        self.block_adj_pos = []     # list of (x,y) of tiles adjacent (horizontal or vertical) to blocks
        self.blocks_showing_num = []# list of (x,y) of blocks showing number of adjacent bulbs
        self.light_up_data = {}      # keeps track of which lightbulbs are lighting what tile(s); it is used to find pos of blocks so that the board has only one solution
        self.BoardDisplayed = False
        self.StretcherAdded = False

        # ------------------------
        # DIFFICULTY SETTINGS - the below parameters affect the difficult of the board! Set wisely
        # block_percentage: Percentage of tiles that are unclickable blocks 
        # light_bulb_near_block_percentage: percentage of lightbulbs adjacent to block out of total # of spaces near blocks
        # grid_size: used for both grid width AND height (so board size = grid_size * grid_size)
        

        #-------------------------
        self.main_sizer.AddStretchSpacer()
        self.main_sizer.Add(self.grid)
        self.main_sizer.AddStretchSpacer()

        self.SetSizer(self.main_sizer)

        # self.Show()
        # self.Layout()
        # self.Update()
        

    #-----------------------------------------------------------------------

    # def SquareWidth(self):
    #     return self.GetClientSize().GetWidth() / Board.BoardWidth

    # def SquareHeight(self):
    #     return self.GetClientSize().GetHeight() / Board.BoardHeight

    def FindPosNearBlock(self, x, y):
        if (x + 1 < self.grid_size and self.board_data[x+1][y] == self.UND and 
            not (x+1, y) in self.block_adj_pos):
            self.block_adj_pos.append((x+1, y))
        if (x - 1 >= 0 and self.board_data[x-1][y] == self.UND and
            not (x-1, y) in self.block_adj_pos):
            self.block_adj_pos.append((x-1, y))
        if (y + 1< self.grid_size and self.board_data[x][y+1] == self.UND and
            not (x, y+1) in self.block_adj_pos):
            self.block_adj_pos.append((x, y+1))
        if (y - 1 >= 0 and self.board_data[x][y-1] == self.UND and 
            not (x, y-1) in self.block_adj_pos):
            self.block_adj_pos.append((x, y-1))

    def FindTilesLit(self, x, y, tile_list):
        # similar to LightAll(), determines which tiles will be lit up when 
        # a lightbult is placed at the given pos (x,y)

        for i in range(y, len(self.board_data)):
            if (self.board_data[x][i] == self.BLOCK):
                # pause if there's a block
                break
            if ((x,i) in tile_list):
                tile_list.remove((x,i))
        
        for i in range(y, -1, -1):
            if (self.board_data[x][i] == self.BLOCK):
                # pause if there's a block
                break
            if ((x,i) in tile_list):
                tile_list.remove((x,i))

        for i in range(x, len(self.board_data)):
            if (self.board_data[i][y] == self.BLOCK):
                # pause if there's a block
                break
            if ((i,y) in tile_list):
                tile_list.remove((i,y))

        for i in range(x, -1, -1):
            if (self.board_data[i][y] == self.BLOCK):
                # pause if there's a block
                break
            if ((i,y) in tile_list):
                tile_list.remove((i,y))
    
    def FillLightUpData(self, x, y):
        # similar to LightAll(), determines how many lightbulbs will light up each tile given 
        # a lightbult is placed at the given pos (x,y)

        for i in range(y+1, self.grid_size):
            if (self.board_data[x][i] == self.BLOCK):
                # pause if there's a block
                break
            if ((x,i) in self.light_up_data):
                self.light_up_data[(x,i)].append((x,y))
            else:
                self.light_up_data[(x,i)] = [(x,y)]
        
        for i in range(y-1, -1, -1):
            if (self.board_data[x][i] == self.BLOCK):
                # pause if there's a block
                break
            if ((x,i) in self.light_up_data):
                self.light_up_data[(x,i)].append((x,y))
            else:
                self.light_up_data[(x,i)] = [(x,y)]

        for i in range(x+1, self.grid_size):
            if (self.board_data[i][y] == self.BLOCK):
                # pause if there's a block
                break
            if ((i,y) in self.light_up_data):
                self.light_up_data[(i,y)].append((x,y))
            else:
                self.light_up_data[(i,y)] = [(x,y)]

        for i in range(x-1, -1, -1):
            if (self.board_data[i][y] == self.BLOCK):
                # pause if there's a block
                break
            if ((i,y) in self.light_up_data):
                self.light_up_data[(i,y)].append((x,y))
            else:
                self.light_up_data[(i,y)] = [(x,y)]

    def SetDifficulty(self):
        # block_percentage: % of blocks out of total tiles
        # light_bulb_near_block: number of lightbulbs out of total tiles adjacent to blocks
        # numbers_shown: % of blocks showing number of adjacent lightbulbs

        if (self.main_frame.info.diff_options.GetStringSelection() == "Easy"):
            self.block_percentage = 0.3              
            self.light_bulb_near_block_percentage = 0.4
            self.numbers_shown_percentage = 0.8
        else:
            self.block_percentage = 0.2          
            self.light_bulb_near_block_percentage = 0.3
            self.numbers_shown_percentage = 0.65
    
    def SetBoardSize(self):
        if (self.main_frame.info.size_options.GetStringSelection() == "Small"):
            self.grid_size = SMALL_SIZE     
        elif (self.main_frame.info.size_options.GetStringSelection() == "Medium"):   
            self.grid_size = MEDIUM_SIZE
        else:
            self.grid_size = LARGE_SIZE  

    def CreateBoard(self):
        # create board data that lays out the position of blocks and lightbulbs
        # 3 states: undetermined, block, and lightbulb

        self.SetBoardSize()
        self.SetDifficulty()

        self.InitializeBoardList(self.board_data, -1)
        for i in range(self.grid_size):
            # row = []
            for j in range(self.grid_size):
                # row.append(-1)
                self.available_tiles.append((i, j))
            # self.board_data.append(row)
           
        # arbitrarily find block positions
        for i in range(int(float(self.grid_size * self.grid_size) * self.block_percentage)):
            x, y = random.choice(self.available_tiles)
            self.board_data[x][y] = self.BLOCK
            self.block_pos.append((x, y))
            self.available_tiles.remove((x, y))
        
        # show number of adjacent bulbs on a certain percentage of blocks
        blocks_not_showing = self.block_pos # copyt list

        # randomly decide which blocks will show the number of adjacent tiles
        if (len(self.blocks_showing_num) == 0):
            for i in range(int(len(self.block_pos) * self.numbers_shown_percentage)):
                x, y = random.choice(self.block_pos)
                if ((x,y) in blocks_not_showing):
                    blocks_not_showing.remove((x,y))
                    self.blocks_showing_num.append((x,y))

        # find all positions near blocks
        for i in range(len(self.block_pos)):
            block_x, block_y = self.block_pos[i]
            self.FindPosNearBlock(block_x, block_y)
        
        # set lightbulbs near blocks
        list_size = len(self.block_adj_pos)
        for i in range(int(float(list_size) * self.light_bulb_near_block_percentage)):
            x, y = random.choice(self.block_adj_pos)
            self.board_data[x][y] = self.LIGHT_BULB

            # find light paths and remove from both lists:
            self.FindTilesLit(x,y, self.block_adj_pos)
            self.FindTilesLit(x,y, self.available_tiles)
            
            # print("coords", x,y)
            # for tile in self.block_adj_pos:
            #     print(tile[0], tile[1])

            if (len(self.block_adj_pos) == 0):
                break

        # if there are still tiles not lit up, randomly select one
        # and place a bulb there
        
        # for i in range(len(self.available_tiles)):
        #     print(self.available_tiles[i][0], self.available_tiles[i][1])
        # print("Before: ", len(self.available_tiles))
        

        while (len(self.available_tiles) > 0):
            x, y = random.choice(self.available_tiles)
            self.board_data[x][y] = self.LIGHT_BULB
            if (not self.HasAdjNumberedBlock(x,y)):
                self.FillLightUpData(x,y)
            self.FindTilesLit(x,y, self.available_tiles)
            # print(x, y)
            # print("tiles left", len(self.available_tiles))
        
        for tile_pos, bulb_pos in self.light_up_data.items():
            print(tile_pos, ' -> ', bulb_pos)

        # if there are two ways to light up tiles, remove one
        for tile_pos, bulb_pos in self.light_up_data.items():
            if (len(bulb_pos) > 1):
                # if more than 1 bulb is lighting up the tile, block it so that there's only one way to light up the area
                x = tile_pos[0]
                y = tile_pos[1]
                self.board_data[x][y] = self.LIGHT_BULB
                for bulb in bulb_pos: 
                    # remove bulbs and place one at the intersect
                    self.board_data[bulb[0]][bulb[1]] = -1
                # self.block_pos.append((x,y))

        # for i in range(self.grid_size):
        #     for j in range(self.grid_size):
        #         if (self.light_up_data[i][j] > 1):


    def CheckBoard(self):
        # check if board is complete
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (self.board[i][j].getState() == 1):
                    # detected a tile not lit
                    self.DisplayFailMsg()
                    return
                elif (self.board[i][j].getState() == 0 and self.board[i][j].GetLabel() != "" and
                    self.FindAdjBulbsForCompleteBoard(i,j) != self.board[i][j].getNum()):
                    # the number of lightbulbs placed is wrong
                    self.DisplayFailMsg()
                    return
                    
        self.DisplaySuccessMsg()


    def DisplayFailMsg(self):
        wx.MessageBox("The board is not complete", "Failed!", wx.OK | wx.ICON_ERROR)
    
    def DisplaySuccessMsg(self):
        wx.MessageBox("Board solved!", "Success!", wx.OK | wx.ICON_NONE)

    def SolveBoard(self):
        self.DeleteTiles()
        self.board = []
        self.light_board = []
        self.DisplayBoard()
        self.InitializeBoardList(self.light_board, 0)
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (self.board_data[i][j] == self.LIGHT_BULB):
                    # place lightbulbs where they go
                    self.board[i][j].light_bulb = True
                    self.board[i][j].showLightBulb()
                    self.board[i][j].lightOn()
                    self.board[i][j].lightAll()
                elif (self.board[i][j].light_bulb == True):
                    # remove lightbulb img where it shouldn't be
                    self.light_bulb = False
                    self.board[i][j].removeImg()
        self.Layout()
        self.Update()

    def InitializeBoardList(self, board, init_val):
        # Initialize board (without data)
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size): 
                row.append(init_val)
            board.append(row)

    def FindAdjBulbs(self, x, y):
        bulbs = 0
        if (x + 1 < self.grid_size and self.board_data[x+1][y] == self.LIGHT_BULB):
            bulbs += 1
        if (x - 1 >= 0 and self.board_data[x-1][y] == self.LIGHT_BULB):
            bulbs += 1
        if (y + 1 < self.grid_size and self.board_data[x][y+1] == self.LIGHT_BULB):
            bulbs += 1
        if (y - 1 >= 0 and self.board_data[x][y-1] == self.LIGHT_BULB):
            bulbs += 1

        return bulbs

    def FindAdjBulbsForCompleteBoard(self, x, y):
        bulbs = 0
        if (x + 1 < self.grid_size and self.board[x+1][y].hasLightBulb()):
            bulbs += 1
        if (x - 1 >= 0 and self.board[x-1][y].hasLightBulb()):
            bulbs += 1
        if (y + 1 < self.grid_size and self.board[x][y+1].hasLightBulb()):
            bulbs += 1
        if (y - 1 >= 0 and self.board[x][y-1].hasLightBulb()):
            bulbs += 1

        return bulbs
    
    # determine if there's a numbered block adjacen to the tile
    def HasAdjNumberedBlock(self, x, y):
        if (x + 1 < self.grid_size and (x+1,y) in self.blocks_showing_num):
            return True
        if (x - 1 >= 0 and (x-1,y) in self.blocks_showing_num):
            return True
        if (y + 1 < self.grid_size and (x,y+1) in self.blocks_showing_num):
            return True
        if (y - 1 >= 0 and (x,y-1) in self.blocks_showing_num):
            return True

        return False

    def DisplayBoard(self):
        if (not self.StretcherAdded):
            self.grid.AddStretchSpacer(1)
            self.StretcherAdded = True

        for i in range(self.grid_size):
            tile_row = [] #stores tiles in each row
            bs = wx.BoxSizer(wx.HORIZONTAL)
            for j in range(self.grid_size):
                adj_bulbs = self.FindAdjBulbs(i, j)
        
                # int(bool(board)) is to determine whether there's a block or not. We know a block is positioned there only if board[i][j] is false
                # if (self.board_data[i][j] == 1):
                #     tile = Tile(self, tile_state=self.board_data[i][j], adj_bulbs = adj_bulbs, x=j, y=i, size=(TILE_SIZE,TILE_SIZE))
                # else:
                #     tile = Tile(self, tile_state=self.board_data[i][j], adj_bulbs = adj_bulbs, x=j, y=i, size=(TILE_SIZE,TILE_SIZE))                
                tile = Tile(self, tile_state=int(bool(self.board_data[i][j])), adj_bulbs = adj_bulbs, x=j, y=i, size=(TILE_SIZE,TILE_SIZE))                
                bs.Add(tile, 0, wx.ALL, 0)
                tile_row.append(tile)

            self.grid.Add(bs, wx.CENTER)
            self.board.append(tile_row)
    
        for x,y in (self.blocks_showing_num):
            self.board[x][y].SetLabel(str(self.board[x][y].getNum()))

        self.BoardDisplayed = True

        self.Layout()
        self.Update()

    def DeleteTiles(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                self.board[i][j].Destroy()

    def ResetBoard(self):
        # delete everything
        self.DeleteTiles()
        self.BoardDisplayed = False
        self.board = []
        self.board_data = []
        self.light_board = []
        self.available_tiles = []
        self.block_pos = []
        self.block_adj_pos = [] 
        self.blocks_showing_num = []
        self.light_up_data = {}
        
    def HideBoard(self):
        self.BoardDisplayed = False

class Info(wx.Panel):
    def __init__(self, parent, MainFrame):
        super().__init__(parent=parent)
        self.main_frame = MainFrame

        self.parent = parent
        self.bitmaps_used = list()
        self.tiles_hit = list()

        self.grid_sizer = wx.BoxSizer(wx.VERTICAL)
        text_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Data representation (list of lists) of board
        self.board = self.main_frame.board

        # #text sizers
        row1 = wx.BoxSizer(wx.VERTICAL)
        row2 = wx.BoxSizer(wx.VERTICAL)
        row3 = wx.BoxSizer(wx.VERTICAL)
        row4 = wx.BoxSizer(wx.VERTICAL)

        # create buttons
        self.create_button = wx.Button(self, label = "Create")
        self.create_button.SetSize((BUTTON_WIDTH, BUTTON_HEIGHT))
        self.create_button.Bind(wx.EVT_BUTTON, self.OnCreate)
        row1.Add(self.create_button, 1, wx.ALL, 5)

        self.solve_button = wx.Button(self, label = "Solve")
        self.solve_button.SetSize((BUTTON_WIDTH, BUTTON_HEIGHT))
        self.solve_button.Bind(wx.EVT_BUTTON, self.OnSolve)
        row2.Add(self.solve_button, 1, wx.ALL, 5)

        self.check_button = wx.Button(self, label = "Check")
        self.check_button.SetSize((BUTTON_WIDTH, BUTTON_HEIGHT))
        self.check_button.Bind(wx.EVT_BUTTON, self.OnCheck)
        row3.Add(self.check_button, 1, wx.ALL, 5)

        self.check_button = wx.Button(self, label = "Reset")
        self.check_button.SetSize((BUTTON_WIDTH, BUTTON_HEIGHT))
        self.check_button.Bind(wx.EVT_BUTTON, self.OnReset)
        row4.Add(self.check_button, 1, wx.ALL, 5)

        # difficulty and size selection
        difficulty_list = ["Easy", "Hard"]     
        board_size_list = ["Small", "Medium", "Large"]     
        self.diff_options = wx.RadioBox(self, label = "Difficulty", choices = difficulty_list,
        majorDimension = 1, style = wx.RA_SPECIFY_COLS)
        
        self.size_options = wx.RadioBox(self, label = "Board Size", choices = board_size_list,
        majorDimension = 1, style = wx.RA_SPECIFY_COLS)

        text_sizer.Add(row1, 1, wx.ALL, 5)
        text_sizer.Add(row2, 1, wx.ALL, 5)
        text_sizer.Add(row3, 1, wx.ALL, 5)
        text_sizer.Add(row4, 1, wx.ALL, 5)
        text_sizer.Add(self.size_options, 0, wx.ALL, 5)
        text_sizer.Add(self.diff_options, 0, wx.ALL, 5)

        main_sizer.Add(self.grid_sizer, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        main_sizer.Add(text_sizer, 1, wx.ALL, 5)
        
        self.SetSizer(main_sizer)

    def OnCreate(self, event):
        if (self.board.BoardDisplayed):
            self.board.ResetBoard()
            # self.parent.board = Board(self.parent.sp, self.parent)
            # self.board = self.parent.board

        self.board.CreateBoard()
        self.board.DisplayBoard()
        self.board.InitializeBoardList(self.board.light_board, 0)
    
    def OnSolve(self, event):
        if (self.board.BoardDisplayed):
            self.board.SolveBoard()
    
    def OnCheck(self, event):
        if (self.board.BoardDisplayed):
            self.board.CheckBoard()
    
    def OnReset(self, event):
        if (self.board.BoardDisplayed):
            self.board.DeleteTiles()
            self.board.board = []
            self.board.light_board = []
            self.board.DisplayBoard()
            self.board.InitializeBoardList(self.board.light_board, 0)

if __name__ == '__main__':
    app = wx.App()
    WINDOW_WIDTH, WINDOW_HEIGHT = wx.GetDisplaySize()
    GRID_SIZE = 300
    APP_HEIGHT = 600
    APP_WIDTH = 700
    TILE_SIZE = 35
    BUTTON_HEIGHT = int(WINDOW_HEIGHT / 12)
    BUTTON_WIDTH = int(WINDOW_WIDTH / 12)
    

    frm = MainFrame()
    app.MainLoop()