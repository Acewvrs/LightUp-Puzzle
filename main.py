import wx
import board

APP_HEIGHT = 600
APP_WIDTH = 700
MINIMUM_PANEL_SIZE = 100
INIT_POS = 600

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Light UP Generator', style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER, size=(APP_WIDTH, APP_HEIGHT))
        
        self.sp = wx.SplitterWindow(self)
        self.board = board.Board(self.sp, self)
        self.board.SetBackgroundColour("white")

        self.info = Info(self.sp, self)

        self.sp.SplitVertically(self.board, self.info, INIT_POS)
        self.sp.SetMinimumPaneSize(MINIMUM_PANEL_SIZE)

        self.CenterOnScreen(wx.BOTH)
        self.Show()


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

        # class representing the board
        self.board = self.main_frame.board

        # #text sizers
        row1 = wx.BoxSizer(wx.VERTICAL)
        row2 = wx.BoxSizer(wx.VERTICAL)
        row3 = wx.BoxSizer(wx.VERTICAL)
        row4 = wx.BoxSizer(wx.VERTICAL)
        row5 = wx.BoxSizer(wx.VERTICAL)
        row6 = wx.BoxSizer(wx.VERTICAL)
        row7 = wx.BoxSizer(wx.VERTICAL)

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

        self.check_button = wx.Button(self, label = "Clear")
        self.check_button.SetSize((BUTTON_WIDTH, BUTTON_HEIGHT))
        self.check_button.Bind(wx.EVT_BUTTON, self.OnClear)
        row4.Add(self.check_button, 1, wx.ALL, 5)

        self.save_button = wx.Button(self, label = "Save")
        self.save_button.SetSize((BUTTON_WIDTH, BUTTON_HEIGHT))
        self.save_button.Bind(wx.EVT_BUTTON, self.OnSave)
        row5.Add(self.save_button, 1, wx.ALL, 5)

        self.load_button = wx.Button(self, label = "Load")
        self.load_button.SetSize((BUTTON_WIDTH, BUTTON_HEIGHT))
        self.load_button.Bind(wx.EVT_BUTTON, self.OnLoad)
        row6.Add(self.load_button, 1, wx.ALL, 5)

        self.legup_button = wx.Button(self, label = "Save Board \nfor LEGUP")
        self.legup_button.SetSize((BUTTON_WIDTH, BUTTON_HEIGHT))
        self.legup_button.Bind(wx.EVT_BUTTON, self.OnLegup)
        row7.Add(self.legup_button, 1, wx.ALL, 5)

        # add radiobox for users to select difficulty and size selection
        difficulty_list = ["Easy", "Hard"]     
        board_size_list = ["Small", "Medium", "Large"]     
        self.diff_options = wx.RadioBox(self, label = "Difficulty", choices = difficulty_list,
        majorDimension = 1, style = wx.RA_SPECIFY_COLS)
        
        self.size_options = wx.RadioBox(self, label = "Board Size", choices = board_size_list,
        majorDimension = 1, style = wx.RA_SPECIFY_COLS)

        # add everything into the right text panel
        text_sizer.Add(row1, 1, wx.ALL, 5)
        text_sizer.Add(row2, 1, wx.ALL, 5)
        text_sizer.Add(row3, 1, wx.ALL, 5)
        text_sizer.Add(row4, 1, wx.ALL, 5)
        text_sizer.Add(self.size_options, 0, wx.ALL, 5)
        text_sizer.Add(self.diff_options, 0, wx.ALL, 5)
        text_sizer.Add(row5, 1, wx.ALL, 5)
        text_sizer.Add(row6, 1, wx.ALL, 5)
        text_sizer.Add(row7, 2, wx.VERTICAL, 5)

        # add the text panel and the board into the main sizer
        main_sizer.Add(self.grid_sizer, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        main_sizer.Add(text_sizer, 1, wx.ALL, 5)
        
        self.SetSizer(main_sizer)

    def OnCreate(self, event):
        if (self.board.BoardDisplayed):
            self.board.ResetBoard()

        self.board.FindBoardSize()
        self.board.CreateBoard()
        self.board.DisplayBoard()
        self.board.InitializeBoardList(self.board.light_board, 0)
    
    def OnSolve(self, event):
        if (self.board.BoardDisplayed):
            self.board.SolveBoard()
    
    def OnCheck(self, event):
        if (self.board.BoardDisplayed):
            self.board.CheckBoardIsSolved(True)
    
    def OnClear(self, event):
        # do a soft reset (different than self.board.ResetBoard) as
        # it doesn't create a completely new board
        if (self.board.BoardDisplayed):
            self.board.DeleteTiles()
            self.board.board = []
            self.board.light_board = []
            self.board.DisplayBoard()
            self.board.InitializeBoardList(self.board.light_board, 0)

    def OnSave(self, event):
        if (self.board.BoardDisplayed):
            self.board.SaveBoard(LEGUP=False)
        else:
            self.board.DisplayInitializeBoardMsg()

    def OnLoad(self, event):
        if (self.board.BoardDisplayed):
            self.board.ResetBoard()

        self.board.LoadBoard()
        # self.OnCreate(event)

    def OnLegup(self, event):
        if (self.board.BoardDisplayed):
            self.board.SaveBoard(LEGUP=True)
        else:
            self.board.DisplayInitializeBoardMsg()

if __name__ == '__main__':
    app = wx.App()
    WINDOW_WIDTH, WINDOW_HEIGHT = wx.GetDisplaySize()
    BUTTON_HEIGHT = int(WINDOW_HEIGHT / 12)
    BUTTON_WIDTH = int(WINDOW_WIDTH / 12)
    frm = MainFrame()
    app.MainLoop()
    
