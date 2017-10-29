import gdb

def do(inst):
  gdb.execute(inst, to_string=True)

def setup():

  do('b *0x401AD1')
  do('b *0x401ADB')

def run(input=''):
  


  if len(input) > 0:
    try:
      do('r <<< ' + input)
    except:
      return
  else:
    gdb.execute('r')
  #then we hit the first breakpoint 
  do('b *0x7ffff7df3926')
  do('c')
  #now we hit the above breakpoint



def tryInput(input):
  run(input)
  count = -1
  while 1:
    try:
      do('c')
    except:
      break
      pass
    count += 1
  do('del 3')
  print "Count was {0} for {1}".format(count, input)
  return count

#given the string so far
#find the next character
def nextChar(string):
  cur = tryInput(string)
  charList = ['\\'+chr(x) for x in xrange(ord(' '), ord('~') + 1)]

  #[charList.append(x) for x in xrange(ord('a'), ord('z') + 1)]
  #[charList.append(x) for x in xrange(ord('0'), ord('9') + 1)]
  #[charList.append(x) for x in xrange(ord(' '), ord('9') + 1)]
  for char in charList:
    if tryInput(string + char) > cur:
      return string + char
  return string


def brute():
  string = ''
  newString = nextChar(string)
  while newString != string:
    string = newString
    newString = nextChar(string)

  print "Got to " + string





  # run with gdb r --command pyRun.py
