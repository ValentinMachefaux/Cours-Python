from random import randint

def listX(x):
  L = []
  i=0
  while i<x:
    L.append(randint(0,10))
    i+=1
  return L

from random import randint
def conc_list(x):
    L1 = listX(x)
    L2 = listX(x)
    L3 = []
    #print(L1,L2)
    L3 = L1+L2
    print(L3)
    #return L3
  
conc_list(10)