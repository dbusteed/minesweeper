# TODO
# reset button
# winning check?
# button highlight
# colors (backgound, cells, numbers)
# bitmap buttons


import wx
from random import randint

LEN = 8
MINE_COUNT = 10
GOOD_VAL = []
BTN_SIZE = 40
HEIGHT = BTN_SIZE * LEN + 70  # 50 for top panel, 10x2 for board padding
WIDTH = BTN_SIZE * LEN + 20 # 10x2 for padding
A = []

def get_num(a,m,n):
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

def get_neighbors(m,n):
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

def start_game():
  print('starting game')
  a = [' '] * LEN
  for x in range(LEN):
    GOOD_VAL.append(x)
    a[x] = [' '] * LEN
      
  for i in range(MINE_COUNT):
    #TODO: add checking for 'double mines'
    m,n = randint(0,LEN-1), randint(0,LEN-1)
    a[m][n] = '@'
      
  for m in range(LEN):
    for n in range(LEN):
        a[m][n] = get_num(a,m,n)

  for m in range(LEN):
    for n in range(LEN):
      btn = wx.Button(bottomPanel, pos=(10+m*BTN_SIZE, 10+n*BTN_SIZE), size=(BTN_SIZE,BTN_SIZE), label=(' '), name=(str(m)+'-'+str(n)))
      btn.SetBackgroundColour(wx.Colour(255,255,255))
      btn.Bind(wx.EVT_BUTTON, lambda e, m=m, n=n, b=btn: handle_click(e, m, n, b), btn)
      btn.Bind(wx.EVT_RIGHT_DOWN, lambda e, m=m, n=n, b=btn: handle_right_click(e, m, n, b), btn)

  return a

def call_start_game(self):
  A = start_game()

def handle_click(self, m, n, btn):

  print(A)

  if(A[m][n] == '@'):
    for i in range(LEN):
      for j in range(LEN):
        b = panel.FindWindowByName(str(i)+'-'+str(j))
        if A[i][j] == '@':
          b.SetBackgroundColour(wx.Colour(255, 113, 107))
        else:
          b.SetBackgroundColour(wx.Colour(220,220,220)) 
        b.SetLabel(A[i][j])
        
  elif A[m][n] == ' ':
    open_cells = get_neighbors(m,n)
    for c in open_cells:
      new_neighbors = get_neighbors(c[0],c[1])
      for nn in new_neighbors:
        if nn not in open_cells and A[nn[0]][nn[1]] == ' ':
          open_cells.append(nn)
          
    for c in open_cells:
      b = panel.FindWindowByName(str(c[0])+'-'+str(c[1]))
      b.SetBackgroundColour(wx.Colour(220,220,220))
      b.SetLabel(A[c[0]][c[1]])
      
    for c in open_cells:
      if A[c[0]][c[1]] == ' ':
        for n in get_neighbors(c[0],c[1]):
          if A[n[0]][n[1]] != ' ':
            b = panel.FindWindowByName(str(n[0])+'-'+str(n[1]))
            b.SetBackgroundColour(wx.Colour(220,220,220))
            b.SetLabel(A[n[0]][n[1]])
    
  else: # 1,2,3 etc
    btn.SetBackgroundColour(wx.Colour(220,220,220)) 
    btn.SetLabel(A[m][n])

def handle_right_click(self, m, n, btn):
  if btn.GetLabel() == ' ':
    btn.SetLabel('*')
    btn.SetBackgroundColour(wx.Colour(49, 199, 107))
  elif btn.GetLabel() == '*':
    btn.SetLabel(' ')
    btn.SetBackgroundColour(wx.Colour(255, 255, 255))
    
app = wx.App()
window = wx.Frame(None, title='Minesweeper', size=(WIDTH, HEIGHT))
window.SetMinClientSize((WIDTH,HEIGHT))

panel = wx.Panel(window)
panel.SetBackgroundColour(wx.Colour(226, 226, 226))

topPanel = wx.Panel(panel, pos=(0,0), size=(WIDTH,50))
topPanel.SetBackgroundColour(wx.Colour(196, 196, 196))

bottomPanel = wx.Panel(panel, pos=(0,50), size=(WIDTH,HEIGHT-50))
bottomPanel.SetBackgroundColour(wx.Colour(226, 226, 226))

resetButton = wx.Button(topPanel, pos=(10,10), size=(100,30), label='Reset')
resetButton.Bind(wx.EVT_BUTTON, call_start_game)

# make the grid of buttons
# for m in range(LEN):
#   for n in range(LEN):
#     btn = wx.Button(bottomPanel, pos=(10+m*BTN_SIZE, 10+n*BTN_SIZE), size=(BTN_SIZE,BTN_SIZE), label=(' '), name=(str(m)+'-'+str(n)))
#     btn.SetBackgroundColour(wx.Colour(255,255,255))
#     btn.Bind(wx.EVT_BUTTON, lambda e, m=m, n=n, b=btn: handle_click(e, m, n, b), btn)
#     btn.Bind(wx.EVT_RIGHT_DOWN, lambda e, m=m, n=n, b=btn: handle_right_click(e, m, n, b), btn)

# import wx.lib.inspection
# wx.lib.inspection.InspectionTool().Show()
    
A = start_game()

window.Show(True)
app.MainLoop()