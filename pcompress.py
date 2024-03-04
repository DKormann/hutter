#%%
import json
import zlib
#%%
with open("./book", 'rb') as f:
  book = f.read()
print("book len:",len(book))
print(book[:100])


#%%
def test(cls, data): 
  enc = cls.encode(data)
  print(f"{cls.__name__} encodes {len(data) if getattr(data, '__len__', None) else ''} => {len(enc)}")
  assert type(enc) == bytes
  assert data == cls.decode(enc)

# %%

class Tuple2Bytes:
  def encode(raw: tuple):
    raw = [e if type(e) == bytes else bytes(json.dumps(e),'utf-8') for e in raw]
    header = bytes(json.dumps([len(e) for e in raw]),'utf-8')
    header = bytes([len(header)]) + header
    return header + b''.join(raw)

  def decode(data):
    header = data[1:data[0]+1]
    header = json.loads(header)
    raw = []
    data = data[data[0]+1:]
    for l in header:
      raw.append(data[:l])
      data = data[l:]
    return tuple(raw)

test(Tuple2Bytes, (b"hello",b"world"))

#%%
class Bits2Bytes:
  def encode(raw: list[int]):
    l = len(raw)
    data = []
    raw = raw + [0]*(8-len(raw)%8)
    for i in range(0, len(raw), 8):
      data.append(int("".join(map(str,raw[i:i+8])),2))
    
    return Tuple2Bytes.encode((l, bytes(data)))

  def decode(data):

    l, data = Tuple2Bytes.decode(data)
    l = json.loads(l.decode())
    dec = []
    for b in data:
      b = bin(b)[2:]
      b = '0'*(8-len(b)) + b
      for c in b: dec.append(int(c))
    return dec[:l]

test(Bits2Bytes, [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1])

#%%

class Huffman:
  def encode(raw:bytes):
    charcount = {}
    for c in raw:
      charcount[c] = charcount.get(c,0) + 1
    codes = [(c, charcount[c]) for c in charcount]
    while len(codes) > 1:
      codes = sorted(codes, key=lambda x: x[1])
      codes = [((codes[0][0], codes[1][0]), codes[0][1]+codes[1][1])]+codes[2:]

    tree = codes[0][0]

    b2c = {}
    def _tree(codes, prefix = []):
      if type(codes) == int:
        b2c[codes] = prefix
        return
      _tree(codes[0], prefix+[0])
      _tree(codes[1], prefix+[1])
    _tree(tree)

    enc = []
    for c in raw:
      enc.extend(b2c[c])
    enc = Bits2Bytes.encode(enc)
    print('code len:',len(enc))

    return Tuple2Bytes.encode((tree, enc))

  def decode(data:bytes):
    tree, enc = Tuple2Bytes.decode(data)
    tree = json.loads(tree.decode())
    enc = Bits2Bytes.decode(enc)
    dec = []
    ptr = tree
    for c in enc:
      ptr = ptr[c]
      if type(ptr) == int:
        dec.append(ptr)
        ptr = tree
    return bytes(dec)

test(Huffman, b'hello world')
test(Huffman, book)


# %%

class Zlib:
  def encode(raw:bytes):
    return zlib.compress(raw)

  def decode(data:bytes):
    return zlib.decompress(data)

test(Zlib, book)
# %%


class PRoller:

  def __init__(self):

    self.encoding = []
    self.p = 0
    self.margin = 2

    self.p2 = 0
    self.margin2 = 1
    self.ptr2 = 0
    self.s2 = 1

  def encode(self, p:float, margin:float):

    self.p += p * self.margin
    self.margin *= margin

    if self.encoding != []:
      self.encoding.pop()
      self.p /= 2
      self.margin /= 2
      self.p += 1

    while 0 < self.p:
      if 1 < self.p + self.margin:
        self.p -=1
        self.encoding += [1]
      else:
        self.encoding += [0]
      self.p *= 2
      self.margin *= 2
    print (self.encoding)
  
  def decode(self, ps:list[float]):

    cum = [self.p2]
    for p in ps: cum += [cum [-1] + p * self.margin2]

    while True:
      for i in range(len(cum)-1): 
        if self.ptr2 >= cum[i] and cum[i+1] > self.ptr2 + self.s2:
          self.p2 = cum[i]
          self.margin2 *= ps[i]
          return i
      self.s2 /= 2
      
      if self.encoding[0] == 1:
        self.ptr2 += self.s2
      self.encoding = self.encoding[1:]
      if len(self.encoding) == 0: 
        for i in range(len(cum)-1): 
          if self.ptr2 >= cum[i] and cum[i+1] > self.ptr2: return i

roller = PRoller()
roller.encode(0.6,0.01)
roller.encode(0.2,0.005)
assert roller.encoding == [1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1]
print(roller.encoding)

d1 = roller.decode([0.6,0.01,0.3, 0.09])
assert d1 == 1
d2 = roller.decode([0.1,0.1,0.005,0.7, 0.005])

assert d2 == 2


# %%

import io
import sys

def call(code:str):
  orig_stdout = sys.stdout
  sys.stdout = io.StringIO()
  exec(code)
  res = sys.stdout.getvalue()
  sys.stdout = orig_stdout
  return res

call('print("hello world")')


#%%
import inspect

def f():
  print("hello world")

code = inspect.getsource(f)

call(code+"\nf()")