# FLcompress: Data Compression and Decompression Tool
![flcompress-logo](./assets/logo.png)

## Description

<p>
FLcompress is a specialized file compression and decompression tool designed mainly for plain text, including programming files and text files. The tool employs the Huffman algorithm, assigning smaller binary codes to frequently occurring characters and larger codes to those that appear less frequently. This optimization is facilitated through binary trees and a min-heap priority queue, prioritizing characters based on their frequency and organizing them into a tree structure during traversal.

This approach results in a ~2:1 compression ratio, reducing the string size by approximately 50%! Additionally, the tool generates a serialized string representing the Huffman tree in postorder notation for decompression. All necessary decompression data is efficiently packed as binary digits within the compressed file, seamlessly unpacked during the decompression process.

Upon compression, the tool creates a newly generated directory with a random name at the same location as the original file. The compressed file, marked with a ".huff" extension, is placed within this directory. Only files with this extension can undergo decompression. This systematic approach ensures both efficient file management and reliable compression and decompression processes.

For user convenience, we additionally designed a Graphical User Interface (GUI) built with Tkinter for FLcompress.
</p>

<p>
  <img src="assets\GUI.png" width="350" title="FLcompress GUI" style="display: block; margin: 0 auto">
</p>

## Authors 

Harshavardan Yuvaraj ([LinkedIn](https://www.linkedin.com/in/harsha-yuvaraj/))
<br>
Arjun Agarwal ([LinkedIn](https://www.linkedin.com/in/agw02/))

