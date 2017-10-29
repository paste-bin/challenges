import gdb
import re

def do(inst):
  gdb.execute(inst, to_string=True)

def setup():
  do('b *0x0401fbe')


def run(input='AAA'):
  do('r <<< ' + input)
  result = gdb.execute('x/1s *$rax', to_string=True)
  m = re.search('\"(.+)\"', result)
  if m:
    print input + '==' + m.group(1)

def brute(pos=0, string="AAA"):
  myList = list(string)

  for c1 in xrange(ord('0'), ord('1') + 1):
    myList[pos] = chr(c1)
    newStr = ''.join(myList)
    run(newStr)

  for c1 in xrange(ord('a'), ord('z') + 1):
    myList[pos] = chr(c1)
    newStr = ''.join(myList)
    run(newStr)

  for c1 in xrange(ord('A'), ord('Z') + 1):
    myList[pos] = chr(c1)
    newStr = ''.join(myList)
    run(newStr)
