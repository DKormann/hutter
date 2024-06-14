#%%
import os
os.makedirs("./archives", exist_ok=True)

with open("./raw/book", 'rb') as f:
  book = f.read()

def encode(raw):
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

  l = len(enc)
  data = []
  enc = enc + [0]*(6-len(enc)%6)
  for i in range(0, len(enc), 6):
    data.append(int("".join(map(str,enc[i:i+6])),2))
  enc = "".join(map(lambda x: chr(x+157),data))
  return enc, l, tree

def d(x,l,tr):
  r = []
  x = map(lambda x: ord(x)-157, x)
  for b in x:
    b = bin(b)[2:]
    b = '0'*(6-len(b)) + b
    for c in b:r.append(int(c))
  enc = r[:l]
  r = []
  n = tr
  for c in enc:
    n = n[c]
    if type(n) == int:
      r+=[n]
      n=tr
  return bytes(r)


enc, l, tree = encode(book)
dec = d(enc,l,tree)
assert dec == book
#%%

import inspect

def archive(book):
  print(f"{len(book)=}")
  enc, l, tree = encode(book)
  print(f"{len(enc)=}")
  code = f"enc=\"{enc}\"\nl={l}\ntree={tree}\n"
  code += inspect.getsource(d)
  code += "print (d(enc,l,tree).decode(),end='')"
  print(f"{len(code)=}")
  return code

arch = archive(book)
arch

with open("./archives/huffman.py", "w") as f:
  f.write(arch)

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

res = unpack(arch)

assert res == book.decode()