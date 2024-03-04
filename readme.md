## mini version of hutter contest
compress the contents of [**hutter price FAQ**](http://prize.hutter1.net/hfaq.htm#about) (~ 60kB text) into pure python with no imports or execs.

## rule
The only rule: compress content of [book](./book) as much as possible. The compressed result must be an executable python file without `import`, `exec` or `open` that prints the exact book content when executed.

look into [huffman.py](./huffman.py) for a simple compression example.


## todos

 - [x] compress book to smaller than original using only python (huffman.py)
 - [ ] compress stronger than standart zip (27KB)
 - [ ] compress down to 25% (is this even possible?)
 
