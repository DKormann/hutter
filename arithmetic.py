#%%
import math
from arithmeticCoder import decode
import inspect
import os

os.makedirs("./archives", exist_ok=True)

with open("./raw/book", 'rb') as f: book = f.read()


#%%
chars = set(book)
chars = bytes(chars)
c2n = {c:i for i,c in enumerate(chars)}
raw = [c2n[c] for c in book]


#%%

charcount = [0]*len(chars)
for i in raw: charcount[i] += 1

d = charcount
S = len(raw)
for i in range(len(d)):
  d[i] /= S
  if i>0: d[i] += d[i-1]
  d[i] = round(d[i],5)
  if i>0: assert d[i] != d[i-1]
  print(d[i],end=",")

#%%

N = len(chars)
def predictor (x,i):return [3e-05,0.00332,0.15797,0.15802,0.15901,0.1593,0.15935,0.16058,0.16468,0.16876,0.16918,0.17939,0.18211,0.19094,0.19218,0.19578,0.19814,0.19944,0.19986,0.20005,0.20056,0.20082,0.2011,0.20157,0.20276,0.20377,0.20382,0.20467,0.2047,0.20593,0.2083,0.20922,0.21114,0.21195,0.21232,0.21297,0.21393,0.21446,0.2175,0.21755,0.218,0.21938,0.22174,0.22264,0.22335,0.2247,0.22495,0.22557,0.22661,0.22878,0.22939,0.22945,0.23071,0.23158,0.2318,0.23183,0.23242,0.23301,0.23334,0.23337,0.29051,0.3023,0.33164,0.35839,0.45317,0.46735,0.48129,0.51065,0.56807,0.5683,0.57227,0.60728,0.62998,0.68505,0.74826,0.76724,0.76826,0.81907,0.87585,0.94092,0.96139,0.96927,0.97956,0.98287,0.99617,0.99785,0.99791,0.99814,0.9982,0.99826,0.99829,0.99852,0.99861,0.99877,0.99886,0.999,0.99905,0.99907,0.99909,0.99932,0.99934,0.99936,0.99939,0.99955,0.99958,1.,]

#%%
from arithmeticCoder import Coder

def decode(enc,predictor,n,bitsn):
  dec = []
  x = map(lambda x: ord(x)-157, enc)
  for b in x:
    b = bin(b)[2:]
    b = '0'*(6-len(b)) + b
    for c in b:dec.append(int(c))

  dec = dec[:bitsn]
  res = []
  coder = Coder()
  coder.dec = dec + [1]
  for i in range(n): res.append(coder.decode(predictor(res,-1)))
  return bytes(chars[i] for i in res).decode()


class Compressor:

  def __init__(self, predictor, raw= book, name = "arithmetic"):

    coder = Coder()
    rawn = len(raw)
    for i,c in enumerate(raw):
      d = predictor(raw, i)
      coder.encode(d, c)
    enc = coder.encoding
    bitsn = len(enc)
    enc = enc + [0]*(6-len(enc)%6)
    data = []

    for i in range(0, len(enc), 6):
      data.append(int("".join(map(str,enc[i:i+6])),2))
    enc = "".join(map(lambda x: chr(x+157),data))
    self.arch = enc

    
    self.code = f"chars = {repr(chars)}\n"
    self.code += f"enc=\"{enc}\"\n"
    self.code += f"bitsn={bitsn}\n"
    self.code += f"rawn={rawn}\n"
    self.code += inspect.getsource(Coder)
    self.code += inspect.getsource(decode)
    self.code += inspect.getsource(predictor)
    self.code += "print (decode(enc,predictor,rawn,bitsn),end='')"
    print(f"{len(raw)=}")
    print(f"{len(enc)=}")
    print(f"{len(self.code)=}")
    
comp = Compressor(predictor,raw)

with open("./archives/arithmetic.py", "w") as f: f.write(comp.code)

import io
from contextlib import redirect_stdout

def unpack(arch):
  assert "import" not in arch
  assert "exec" not in arch
  assert "eval" not in arch
  assert "open" not in arch
  with io.StringIO() as buf, redirect_stdout(buf):
    exec(arch, {})
    output = buf.getvalue()
  return output

res = unpack(comp.code)

assert res == book.decode()

# %%
