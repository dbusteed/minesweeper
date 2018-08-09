#TODO
#double mines
#check for win
#reset
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
    
    self.A = []
    self.btns = []
    
    self.blank_tile = self.scale_bitmap(wx.Image('./assets/blank_tile.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), BTN_SIZE, BTN_SIZE)
    self.flag_tile = self.scale_bitmap(wx.Image('./assets/flag_tile.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), BTN_SIZE, BTN_SIZE)
    self.clicked_tile = self.scale_bitmap(wx.Image('./assets/clicked_tile.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), BTN_SIZE, BTN_SIZE)
    self.one = self.scale_bitmap(wx.Image('./assets/1.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), BTN_SIZE, BTN_SIZE)
    self.two = self.scale_bitmap(wx.Image('./assets/2.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), BTN_SIZE, BTN_SIZE)
    self.three = self.scale_bitmap(wx.Image('./assets/3.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), BTN_SIZE, BTN_SIZE)
    self.four = self.scale_bitmap(wx.Image('./assets/4.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), BTN_SIZE, BTN_SIZE)
    self.five = self.scale_bitmap(wx.Image('./assets/5.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), BTN_SIZE, BTN_SIZE)
    self.six = self.scale_bitmap(wx.Image('./assets/6.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), BTN_SIZE, BTN_SIZE)
    self.seven = self.scale_bitmap(wx.Image('./assets/7.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), BTN_SIZE, BTN_SIZE)
    self.eight = self.scale_bitmap(wx.Image('./assets/8.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), BTN_SIZE, BTN_SIZE)
    self.nine = self.scale_bitmap(wx.Image('./assets/9.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), BTN_SIZE, BTN_SIZE)
    self.mine_tile = self.scale_bitmap(wx.Image('./assets/mine_tile.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), BTN_SIZE, BTN_SIZE)
    self.red_mine_tile = self.scale_bitmap(wx.Image('./assets/red_mine_tile.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), BTN_SIZE, BTN_SIZE)
    
    btn = wx.Button(self, label='Reset', pos=(10,10), size=(100,30))
    btn.Bind(wx.EVT_BUTTON, lambda e: self.start_game(e))
    
    self.start_game()
   
    i = 0
    for m in range(LEN):
      for n in range(LEN):
        btn = wx.StaticBitmap(self, -1, self.blank_tile, pos=(10+m*BTN_SIZE,50+n*BTN_SIZE))
        btn.SetLabel(str(i)+'-blank')
        btn.Bind(wx.EVT_LEFT_DOWN, lambda e, i=i, m=m, n=n: self.handle_click(e,i,m,n))
        btn.Bind(wx.EVT_RIGHT_DOWN, lambda e, i=i, m=m, n=n: self.handle_right_click(e,i,m,n))
        self.btns.append(btn)
        i += 1
  
  def test(self, event):
    print('asdf')
  
  def scale_bitmap(self, bitmap, width, height):
    image = bitmap.ConvertToImage()
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = image.ConvertToBitmap()
    return result
      
  def start_game(self=None, event=None):
    
    try:
      for m in range(LEN):
        for n in range(LEN):
          i = self.get_i(m,n)          
          self.btns[i] = wx.StaticBitmap(self, -1, self.blank_tile, pos=(10+m*BTN_SIZE,50+n*BTN_SIZE))
          self.btns[i].SetLabel(str(i)+'-blank')    
    except:
      pass
  
    a = [' '] * LEN
    for x in range(LEN):
      GOOD_VAL.append(x)
      a[x] = [' '] * LEN
    
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
        
    self.A = a
        
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
    val = self.A[m][n]
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
    
  def handle_click(self,e,i,m,n):
  
    # for bombs
    if(self.A[m][n] == '@'):      
      for x in range(LEN*LEN):
        cord = self.get_mn(x)
        bmp = self.get_bmp(cord[0], cord[1])
        self.btns[x] = wx.StaticBitmap(self, -1, bmp, pos=(10+cord[0]*BTN_SIZE,50+cord[1]*BTN_SIZE))
        
      self.btns[i] = wx.StaticBitmap(self, -1, self.red_mine_tile, pos=(10+m*BTN_SIZE,50+n*BTN_SIZE))
          
    # for blank spaces
    elif self.A[m][n] == ' ':
      open_cells = self.get_neighbors(m,n)
      for c in open_cells:
        new_neighbors = self.get_neighbors(c[0],c[1])
        for nn in new_neighbors:
          if nn not in open_cells and self.A[nn[0]][nn[1]] == ' ':
            open_cells.append(nn)
            
      for c in open_cells:
        x = self.get_i(c[0],c[1])
        self.btns[x] = wx.StaticBitmap(self, -1, self.get_bmp(c[0],c[1]), pos=(10+c[0]*BTN_SIZE,50+c[1]*BTN_SIZE))
        
      for c in open_cells:
        if self.A[c[0]][c[1]] == ' ':
          for n in self.get_neighbors(c[0],c[1]):
            if self.A[n[0]][n[1]] != ' ':
              x = self.get_i(n[0],n[1])
              self.btns[x] = wx.StaticBitmap(self, -1, self.get_bmp(n[0],n[1]), pos=(10+n[0]*BTN_SIZE,50+n[1]*BTN_SIZE))
      
    # for 1,2,3 etc  
    else: 
      self.btns[i] = wx.StaticBitmap(self, -1, self.get_bmp(m,n), pos=(10+m*BTN_SIZE,50+n*BTN_SIZE))
  
  def handle_right_click(self,e,i,m,n):
    if self.btns[i].GetLabel().split('-')[1] == 'flag':
      self.btns[i] = wx.StaticBitmap(self, -1, self.blank_tile, pos=(10+m*BTN_SIZE,50+n*BTN_SIZE))
      self.btns[i].SetLabel(str(i)+'-blank')
    else:
      self.btns[i] = wx.StaticBitmap(self, -1, self.flag_tile, pos=(10+m*BTN_SIZE,50+n*BTN_SIZE))
      self.btns[i].SetLabel(str(i)+'-flag')
  
  def get_mn(self, i):
    m = i // LEN
    n = i % LEN
    return [m,n]
    
  def get_i(self,m,n):
    return m * LEN + n
  
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
  frame = Frame()  
  app.MainLoop()