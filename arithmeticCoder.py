#%%
import random
#%%

class Coder:
  def __init__(self):
    self.encoding = []
    self.low,self.high = 0,1

  def encode(self, ranges, choice):
    low ,high =([0]+ranges)[choice:choice+2]
    range     =-self.low + self.high
    self.high = self.low + high * range
    self.low  = self.low + low * range
    while True:
      bit = 1 * (0.5 < self.high)
      if self.low - bit *0.5< 0: break
      self.low = self.low * 2 - bit
      self.high = self.high * 2 - bit
      self.encoding.append(bit)

  def decode(self, ranges):
    a = self.dec[len(self.encoding):len(self.encoding)+32]
    tar = int("".join(map(str,a)),2)*2**-len(a)
    target = (tar - self.low) / (self.high - self.low)
    res = len(ranges) - 1
    for i,p in enumerate(ranges):
      res = i
      if p > target:break
    self.encode(ranges, res)
    return res

def decode(bits,predictor,n):
  res = []
  coder = Coder()
  coder.dec = bits + [1]
  for i in range(n): res.append(coder.decode(predictor(res,-1)))
  return res

if __name__ == "__main__":

  predictor = lambda x,i: [i/100 for i in range(1,101)]
  random.seed(0)
  n = 100
  n = 100_000
  choices = [random.randint(0,99) for i in range(n)]

  coder = Coder()
  for c in choices: coder.encode(predictor(choices,-1),c)

  res = decode(coder.encoding, predictor, n)
  assert res == choices
