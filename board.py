import wx
import random
import tile

# physical size of tiles (buttons)
TILE_SIZE = 35

# board width and height
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
        # DIFFICULTY SETTINGS - the below parameters affect the difficult of the board
        # block_percentage: Percentage of tiles that are unclickable blocks 
        # light_bulb_near_block_percentage: percentage of lightbulbs adjacent to block out of total # of spaces near blocks
        # grid_size: used for both grid width AND height (so board size = grid_size * grid_size)
        

        #-------------------------
        self.main_sizer.AddStretchSpacer()
        self.main_sizer.Add(self.grid)
        self.main_sizer.AddStretchSpacer()

        self.SetSizer(self.main_sizer)

    #-----------------------------------------------------------------------

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
        # and remove those tiles from the list
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
            # self.block_percentage = 0.3              
            # self.light_bulb_near_block_percentage = 0.5
            # self.numbers_shown_percentage = 0.8
            self.block_percentage = random.uniform(0.25, 0.35)         
            self.light_bulb_near_block_percentage = random.uniform(0.7, 0.9)  
            self.numbers_shown_percentage = random.uniform(0.8, 0.9)  
        else:
            # self.block_percentage = 0.2          
            # self.light_bulb_near_block_percentage = 0.5
            # self.numbers_shown_percentage = 0.6
            self.block_percentage = 0.25     
            self.light_bulb_near_block_percentage = random.uniform(0.6, 0.7)  
            self.numbers_shown_percentage = random.uniform(0.7, 0.8)
    
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
            for j in range(self.grid_size):
                self.available_tiles.append((i, j))
           
        # arbitrarily find block positions
        for i in range(int(float(self.grid_size * self.grid_size) * self.block_percentage)):
            x, y = random.choice(self.available_tiles)
            self.board_data[x][y] = self.BLOCK
            self.block_pos.append((x, y))
            self.available_tiles.remove((x, y))
        
        # show number of adjacent bulbs on a certain percentage of blocks
        blocks_not_showing = self.block_pos # copy list

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
            if ((block_x, block_y) in self.blocks_showing_num):
                self.FindPosNearBlock(block_x, block_y)
        
        # set lightbulbs near blocks
        list_size = len(self.block_adj_pos)
        for i in range(int(float(list_size) * self.light_bulb_near_block_percentage)):
            x, y = random.choice(self.block_adj_pos)
            self.board_data[x][y] = self.LIGHT_BULB

            # find light paths and remove from both lists:
            self.FindTilesLit(x,y, self.block_adj_pos)
            self.FindTilesLit(x,y, self.available_tiles)

            if (len(self.block_adj_pos) == 0):
                break

             
        # fill out the rest of the board with bulbs so that every tile is lit and the board has (ideally) one solution.
        board_complete = False # check if we've made a completely lit up board with only one solution
        temp_light_pos = []
        iterationMax = 100
        iterationCounter = 0
        while (not board_complete):
            tiles_available = self.available_tiles.copy() # copy available tiles list
            self.light_up_data.clear()
            temp_light_pos.clear()

            # if there are still tiles not lit up, randomly select one
            # and place a bulb there  
            while (len(tiles_available) > 0):
                x, y = random.choice(tiles_available)
                temp_light_pos.append((x,y))
                self.board_data[x][y] = self.LIGHT_BULB
                if (not self.HasAdjNumberedBlock(x,y)):
                    self.FillLightUpData(x,y)
                self.FindTilesLit(x,y, tiles_available)

            # check if there are two ways to light up tiles
            # if there is, start over with the same set of tiles (in self.available_siles)
            one_solution = True
            for tile_pos, bulb_pos in self.light_up_data.items():
                if (len(bulb_pos) > 1):
                    one_solution = False
                    break

            if (one_solution or iterationCounter == iterationMax):
                board_complete = True
            else:
                # remove lightbulbs placed earlier
                for pos in temp_light_pos:
                    self.board_data[pos[0]][pos[1]] = -1
                iterationCounter += 1

        self.available_tiles.clear()


    def CheckBoard(self):
        # check if board is complete
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (self.board[i][j].getState() == 1):
                    # detected an unlit tile
                    self.DisplayFailMsg()
                    return
                elif (self.board[i][j].getState() == 0 and self.board[i][j].GetLabel() != "" and
                    self.FindAdjBulbsForCompleteBoard(i,j) != self.board[i][j].getNum()):
                    # the number of lightbulbs placed near a numbered tile is wrong
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
        # given the position of a tile on the board, find the number of lightbulbs
        # adjacent to that tile.
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
        # start creating tiles and show the board to the user

        if (not self.StretcherAdded):
            self.grid.AddStretchSpacer(1)
            self.StretcherAdded = True

        for i in range(self.grid_size):
            tile_row = [] #stores tiles in each row
            bs = wx.BoxSizer(wx.HORIZONTAL)
            for j in range(self.grid_size):
                adj_bulbs = self.FindAdjBulbs(i, j)
                t = tile.Tile(self, tile_state=int(bool(self.board_data[i][j])), adj_bulbs = adj_bulbs, x=j, y=i, size=(TILE_SIZE,TILE_SIZE))                
                bs.Add(t, 0, wx.ALL, 0)
                tile_row.append(t)

            self.grid.Add(bs, wx.CENTER)
            self.board.append(tile_row)
    
        for x,y in (self.blocks_showing_num):
            self.board[x][y].SetLabel(str(self.board[x][y].getNum()))

        self.BoardDisplayed = True

        self.Layout()
        self.Update()

    def DeleteTiles(self):
        # delete all the tiles on the board (for garbage collection)
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
