#TODO
#double mines
#check for win
#bitmap buttons
#colors (numbers too)


from random import randint
import wx

LEN = 8
MINE_COUNT = 10
GOOD_VAL = []
BTN_SIZE = 40
HEIGHT = BTN_SIZE * LEN + 70
WIDTH = BTN_SIZE * LEN + 20
    
class MainPanel(wx.Panel):
  
  def __init__(self, parent):
    wx.Panel.__init__(self, parent)
    
    self.A = []
    
    btn = wx.Button(self, label='Reset', pos=(10,10), size=(100,30))
    btn.Bind(wx.EVT_BUTTON, lambda e: self.start_game(e))
    
    # flag = wx.Image("./assets/flag.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    # wx.StaticBitmap(self, -1, flag)
    
    self.start_game()
   
    for m in range(LEN):
      for n in range(LEN):
        btn = wx.Button(self, pos=(10+m*BTN_SIZE,50+n*BTN_SIZE), size=(BTN_SIZE,BTN_SIZE), label=(' '), name=(str(m)+'-'+str(n)))
        btn.SetBackgroundColour(wx.Colour(255,255,255))
        btn.Bind(wx.EVT_BUTTON, lambda e, m=m, n=n, b=btn: self.handle_click(e,m,n,b))
        btn.Bind(wx.EVT_RIGHT_DOWN, lambda e, m=m, n=n, b=btn: self.handle_right_click(e,m,n,b))
      
  def start_game(self=None, event=None):
    
    try:
      for m in range(LEN):
        for n in range(LEN):
          btn = self.FindWindowByName(str(m)+'-'+str(n))
          btn.SetBackgroundColour(wx.Colour(255,255,255))
          btn.SetLabel(' ')
    except:
      pass
  
    a = [' '] * LEN
    for x in range(LEN):
      GOOD_VAL.append(x)
      a[x] = [' '] * LEN
    
    for i in range(MINE_COUNT):
      #TODO check for double mines
      m,n = randint(0,LEN-1), randint(0,LEN-1)
      a[m][n] = '@'
      
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
  
  def handle_click(self,e,m,n,btn):
  
    if(self.A[m][n] == '@'):
      for i in range(LEN):
        for j in range(LEN):
          b = self.FindWindowByName(str(i)+'-'+str(j))
          if self.A[i][j] == '@':
            b.SetBackgroundColour(wx.Colour(255, 113, 107))
          else:
            b.SetBackgroundColour(wx.Colour(220,220,220)) 
          b.SetLabel(self.A[i][j])
          
    elif self.A[m][n] == ' ':
      open_cells = self.get_neighbors(m,n)
      for c in open_cells:
        new_neighbors = self.get_neighbors(c[0],c[1])
        for nn in new_neighbors:
          if nn not in open_cells and self.A[nn[0]][nn[1]] == ' ':
            open_cells.append(nn)
            
      for c in open_cells:
        b = self.FindWindowByName(str(c[0])+'-'+str(c[1]))
        b.SetBackgroundColour(wx.Colour(220,220,220))
        b.SetLabel(self.A[c[0]][c[1]])
        
      for c in open_cells:
        if self.A[c[0]][c[1]] == ' ':
          for n in self.get_neighbors(c[0],c[1]):
            if self.A[n[0]][n[1]] != ' ':
              b = self.FindWindowByName(str(n[0])+'-'+str(n[1]))
              b.SetBackgroundColour(wx.Colour(220,220,220))
              b.SetLabel(self.A[n[0]][n[1]])
      
    else: # 1,2,3 etc
      btn.SetBackgroundColour(wx.Colour(220,220,220)) 
      btn.SetLabel(self.A[m][n])
  
  def handle_right_click(self,e,m,n,btn):
  
    if btn.GetLabel() == ' ':
      btn.SetLabel('*')
      btn.SetBackgroundColour(wx.Colour(49, 199, 107))
    elif btn.GetLabel() == '*':
      btn.SetLabel(' ')
      btn.SetBackgroundColour(wx.Colour(255, 255, 255))
  
class Frame(wx.Frame):
  
  def __init__(self):
    wx.Frame.__init__(self, None, title='Minesweeper', size=(WIDTH, HEIGHT))
    self.SetMinClientSize((WIDTH,HEIGHT))
    
    panel = MainPanel(self)
    panel.SetSize((WIDTH, HEIGHT))
    panel.SetBackgroundColour(wx.Colour(226, 226, 226))
    
    self.Show()

if __name__ == '__main__':
  app = wx.App(False)
  frame = Frame()
  app.MainLoop()