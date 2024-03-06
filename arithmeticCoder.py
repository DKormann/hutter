#%%

import itertools
import bisect
import time
import random
from temp.timer import Timer
#%%
def debin(a):
  a = a[:32]
  res= int("".join(map(str,a)),2)*2**-len(a) if a else 0
  return res

class ArithmeticCoder:
  def __init__(self):
    self.encoding = []
    self.low = 0
    self.high = 1

  def encode(self, low:float, high:float):
    range     =-self.low + self.high
    self.high = self.low + high * range
    self.low  = self.low + low * range
    while True:
      bit = 1 * (0.5 < self.high)
      if self.low - bit *0.5< 0: break
      self.low = self.low * 2 - bit
      self.high = self.high * 2 - bit
      self.encoding.append(bit)

  def finish(self):
    self.dec = self.encoding + [1]
    self.__init__()
    self.p = 0
    self.s = 1

  def decode(self, ps):
    if len(self.encoding)!=0:
      tar = self.dec[len(self.encoding):len(self.encoding)+32]
      target = debin(tar)
      target -= self.low
      target /= self.high - self.low

    else: target = debin(self.dec)

    res = len(ps) - 1
    for i,p in enumerate(ps):
      if p > target:
        res = i-1
        break
    self.encode(ps[res],ps[res+1] if res+1 < len(ps) else 1)
    return res

Timer.reset()
random.seed(0)
options = [i/10 for i in range(10)]
coder = ArithmeticCoder()

n = 100_000
choices = [random.randint(0,9) for _ in range(n)]
coder = ArithmeticCoder()

for c in choices: coder.encode(c/10, (c+1)/10)
coder.finish()
decoding = []
for _ in range(n):
  dec = coder.decode(options)
  decoding.append(dec)

Timer.print()
#%%
