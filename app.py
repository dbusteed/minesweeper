#TODO
#check for win
#dynamic
#optimize render?
#refacor self.btns to [][]


from random import randint
import wx

LEN = 8
MINE_COUNT = 10
GOOD_VAL = []
BTN_SIZE = 35
HEIGHT = BTN_SIZE * LEN + 70
WIDTH = BTN_SIZE * LEN + 20
    
class MainPanel(wx.Panel):
  
  def __init__(self, parent):
    wx.Panel.__init__(self, parent)
    
    self.board = []
    self.btns = []
    self.click_count = 0
    self.game_count = 0
    
    self.blank_tile = self.scale_bitmap(wx.Image('./assets/blank_tile.png', wx.BITMAP_TYPE_ANY), BTN_SIZE, BTN_SIZE)
    self.flag_tile = self.scale_bitmap(wx.Image('./assets/flag_tile.png', wx.BITMAP_TYPE_ANY), BTN_SIZE, BTN_SIZE)
    self.clicked_tile = self.scale_bitmap(wx.Image('./assets/clicked_tile.png', wx.BITMAP_TYPE_ANY), BTN_SIZE, BTN_SIZE)
    self.one = self.scale_bitmap(wx.Image('./assets/1.png', wx.BITMAP_TYPE_ANY), BTN_SIZE, BTN_SIZE)
    self.two = self.scale_bitmap(wx.Image('./assets/2.png', wx.BITMAP_TYPE_ANY), BTN_SIZE, BTN_SIZE)
    self.three = self.scale_bitmap(wx.Image('./assets/3.png', wx.BITMAP_TYPE_ANY), BTN_SIZE, BTN_SIZE)
    self.four = self.scale_bitmap(wx.Image('./assets/4.png', wx.BITMAP_TYPE_ANY), BTN_SIZE, BTN_SIZE)
    self.five = self.scale_bitmap(wx.Image('./assets/5.png', wx.BITMAP_TYPE_ANY), BTN_SIZE, BTN_SIZE)
    self.six = self.scale_bitmap(wx.Image('./assets/6.png', wx.BITMAP_TYPE_ANY), BTN_SIZE, BTN_SIZE)
    self.seven = self.scale_bitmap(wx.Image('./assets/7.png', wx.BITMAP_TYPE_ANY), BTN_SIZE, BTN_SIZE)
    self.eight = self.scale_bitmap(wx.Image('./assets/8.png', wx.BITMAP_TYPE_ANY), BTN_SIZE, BTN_SIZE)
    self.nine = self.scale_bitmap(wx.Image('./assets/9.png', wx.BITMAP_TYPE_ANY), BTN_SIZE, BTN_SIZE)
    self.mine_tile = self.scale_bitmap(wx.Image('./assets/mine_tile.png', wx.BITMAP_TYPE_ANY), BTN_SIZE, BTN_SIZE)
    self.red_mine_tile = self.scale_bitmap(wx.Image('./assets/red_mine_tile.png', wx.BITMAP_TYPE_ANY), BTN_SIZE, BTN_SIZE)
    
    reset_bmp = self.scale_bitmap(wx.Image('./assets/reset.png', wx.BITMAP_TYPE_ANY), 80, 40)
    reset_btn = wx.StaticBitmap(self, -1, reset_bmp, pos=(10,10))
    reset_btn.Bind(wx.EVT_LEFT_DOWN, lambda e: self.start_game(e))
    
    self.start_game()
    
    for m in range(LEN):
      for n in range(LEN):
        btn = wx.StaticBitmap(self, -1, self.blank_tile, pos=(10+m*BTN_SIZE,50+n*BTN_SIZE))
        btn.SetLabel('blank')
        btn.Bind(wx.EVT_LEFT_DOWN, lambda e, m=m, n=n: self.handle_click(e,m,n))
        btn.Bind(wx.EVT_RIGHT_DOWN, lambda e, m=m, n=n: self.handle_right_click(e,m,n))
        self.board[m][n].extend([btn, self.get_bmp(m,n)])
  
  def scale_bitmap(self, image, width, height):
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = image.ConvertToBitmap()
    return result
      
  def start_game(self=None, event=None):
    
    self.click_count = 0
    
    if self.game_count > 0:
      print(self.board[0][0])
      for m in range(LEN):
        for n in range(LEN):     
          self.board[m][n][1] = wx.StaticBitmap(self, -1, self.blank_tile, pos=(10+m*BTN_SIZE,50+n*BTN_SIZE))
          self.board[m][n][1].SetLabel('blank')    
          
    self.game_count += 1
  
    # make the underlying board
    a = [[' ']] * LEN
    for x in range(LEN):
      GOOD_VAL.append(x)
      a[x] = [[' ']] * LEN
    
    for i in range(MINE_COUNT):
      alreadyMine = True
      while(alreadyMine):
        m,n = randint(0,LEN-1), randint(0,LEN-1)
        if a[m][n] != '@':
          a[m][n] = '@'
          alreadyMine = False
      
    for m in range(LEN):
      for n in range(LEN):
        a[m][n] = self.get_num(a,m,n)
    
    for m in range(LEN):
      for n in range(LEN):
        a[m][n] = list(a[m][n])
    
    self.board = a
        
  def get_num(self,a,m,n):
    i = 0
      
    if( a[m][n] != '@' ):
      # top left
      if( (m-1 in GOOD_VAL) and (n-1 in GOOD_VAL) ):
        if( a[m-1][n-1] == '@' ):
          i += 1           
      # top center
      if( (m-1 in GOOD_VAL) and (n in GOOD_VAL) ):
        if( a[m-1][n] == '@' ):
          i += 1
      # top right
      if( (m-1 in GOOD_VAL) and (n+1 in GOOD_VAL) ):
        if( a[m-1][n+1] == '@' ):
          i += 1
      # mid left
      if( (m in GOOD_VAL) and (n-1 in GOOD_VAL) ):
        if( a[m][n-1] == '@' ):
          i += 1
      # mid right
      if( (m in GOOD_VAL) and (n+1 in GOOD_VAL) ):
        if( a[m][n+1] == '@' ):
          i += 1
      # bottom left
      if( (m+1 in GOOD_VAL) and (n-1 in GOOD_VAL) ):
        if( a[m+1][n-1] == '@' ):
          i += 1
      # bottom center
      if( (m+1 in GOOD_VAL) and (n in GOOD_VAL) ):
        if( a[m+1][n] == '@' ):
          i += 1 
      # bottom right
      if( (m+1 in GOOD_VAL) and (n+1 in GOOD_VAL) ):
        if( a[m+1][n+1] == '@' ):
          i += 1       

      if(i == 0):
        return ' '
      else:
        return str(i)
        
    else:
      return '@'

  def get_neighbors(self,m,n):
    l = [[m,n]]
    if(m-1 in GOOD_VAL and n-1 in GOOD_VAL):
      l.append([m-1,n-1])
    if(m-1 in GOOD_VAL and n in GOOD_VAL):
      l.append([m-1,n])
    if(m-1 in GOOD_VAL and n+1 in GOOD_VAL):
      l.append([m-1,n+1])
    if(m in GOOD_VAL and n-1 in GOOD_VAL):
      l.append([m,n-1])
    if(m in GOOD_VAL and n+1 in GOOD_VAL):
      l.append([m,n+1])
    if(m+1 in GOOD_VAL and n-1 in GOOD_VAL):
      l.append([m+1,n-1])
    if(m+1 in GOOD_VAL and n in GOOD_VAL):
      l.append([m+1,n])
    if(m+1 in GOOD_VAL and n+1 in GOOD_VAL):
      l.append([m+1,n+1])
    return l
  
  def get_bmp(self,m,n):
    val = self.board[m][n][0]
    if val == '@':
      return self.mine_tile
    elif val == ' ':
      return self.clicked_tile
    elif val == '1':
      return self.one
    elif val == '2':
      return self.two
    elif val == '3':
      return self.three
    elif val == '4':
      return self.four
    elif val == '5':
      return self.five
    elif val == '6':
      return self.six
    elif val == '7':
      return self.seven
    elif val == '8':
      return self.eight
    elif val == '9':
      return self.nine
    
  def handle_click(self,e,m,n):
  
    self.click_count += 1
  
    # for bombs
    if self.board[m][n][0] == '@':
      for a in range(LEN):
        for b in range(LEN):
          self.board[a][b][1] = wx.StaticBitmap(self, -1, self.board[a][b][2], pos=(10+a*BTN_SIZE,50+b*BTN_SIZE))
      
      self.board[m][n][1] = wx.StaticBitmap(self, -1, self.red_mine_tile, pos=(10+m*BTN_SIZE,50+n*BTN_SIZE))
          
    # for blank spaces
    elif self.board[m][n][0] == ' ':
      open_cells = self.get_neighbors(m,n)
      for c in open_cells:
        new_neighbors = self.get_neighbors(c[0],c[1])
        for nn in new_neighbors:
          if nn not in open_cells and self.board[nn[0]][nn[1]][0] == ' ':
            open_cells.append(nn)
            
      for c in open_cells:
        self.board[c[0]][c[1]][1] = wx.StaticBitmap(self, -1, self.board[c[0]][c[1]][2], pos=(10+c[0]*BTN_SIZE,50+c[1]*BTN_SIZE))
        
      for c in open_cells:
        if self.board[c[0]][c[1]][0] == ' ':
          for ne in self.get_neighbors(c[0],c[1]):
            if self.board[ne[0]][ne[1]][0] != ' ':
              self.board[ne[0]][ne[1]][1] = wx.StaticBitmap(self, -1, self.board[ne[0]][ne[1]][2], pos=(10+ne[0]*BTN_SIZE,50+ne[1]*BTN_SIZE))
      
    # for 1,2,3 etc  
    else:
      self.board[m][n][1] = wx.StaticBitmap(self, -1, self.board[m][n][2], pos=(10+m*BTN_SIZE,50+n*BTN_SIZE))
  
  def handle_right_click(self,e,m,n):
    if self.board[m][n][1].GetLabel() == 'flag':
      self.board[m][n][1] = wx.StaticBitmap(self, -1, self.blank_tile, pos=(10+m*BTN_SIZE,50+n*BTN_SIZE))
      self.board[m][n][1].SetLabel('blank')
    else:
      self.board[m][n][1] = wx.StaticBitmap(self, -1, self.flag_tile, pos=(10+m*BTN_SIZE,50+n*BTN_SIZE))
      self.board[m][n][1].SetLabel('flag')
  
class Frame(wx.Frame):
  
  def __init__(self):
    wx.Frame.__init__(self, None, title='Minesweeper', size=(WIDTH, HEIGHT))
    self.SetMinClientSize((WIDTH,HEIGHT))
    
    panel = MainPanel(self)
    panel.SetSize((WIDTH, HEIGHT))
    panel.SetBackgroundColour(wx.Colour(246, 246, 246))
    
    self.Show()

if __name__ == '__main__':
  app = wx.App(False)
  # import wx.lib.inspection
  # wx.lib.inspection.InspectionTool().Show()
  frame = Frame()  
  app.MainLoop()