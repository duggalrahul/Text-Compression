# Text Compression

This implements a frequncy based text compression algorithm. So the most frequently occuring words are replaced by a smaller key throughout text. The initial lines of the compressed text file store the mapping of keys-values. The decode class uses this mapping to replace the keys in the compressed text to regenerate the original text.

## Examples

using the compress class:

```python
c = compress('original_file_name.txt', Num_keys)	
c.compressFile()
c.printFile('compressed_file_name.txt')
```

using the decompress class:

```python
d = decompress('compressed_file_name.txt')	
d.decompressFile()
d.printFile('decompressed_file_name.txt')
```
