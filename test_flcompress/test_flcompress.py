import sys
import os
import unittest

# dynamically resolve root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from compress_utilities import HuffFile, CompressionError

# compressed file extension name
COMPRESSED_FILE_EXTENSION = ".huff"

class TestFLCompress(unittest.TestCase):

    # test if file contents before compression equal file contents after
    # compression and decompression. Small text file ~ 1KB
    def test_flcompress_1(self, filename=os.path.join('test_flcompress','test_small_file.txt')):
        hf = HuffFile()
        with open(filename, "r") as f:
            BEFORE = f.read()

        dir_name = hf.compress_file(filename)
        filename = os.path.join(dir_name, os.path.split(filename)[1])
        
        hf.decompress_file(filename + COMPRESSED_FILE_EXTENSION)

        with open(filename, "r") as f:
            AFTER = f.read()

        self.assertEqual(BEFORE, AFTER)
    
    # test if file contents before compression equal file contents after
    # compression and decompression. Large text file ~ 11.1MB
    def test_flcompress_2(self, filename=os.path.join('test_flcompress','test_large_file.txt')):
        hf = HuffFile()
        with open(filename, "r") as f:
            BEFORE = f.read()

        dir_name = hf.compress_file(filename)
        filename = os.path.join(dir_name, os.path.split(filename)[1])
        hf.decompress_file(filename + COMPRESSED_FILE_EXTENSION)

        with open(filename, "r") as f:
            AFTER = f.read()

        self.assertEqual(BEFORE, AFTER)

    # test if file contents before compression equal file contents after
    # compression and decompression. Large html file ~ 356KB
    def test_flcompress_3(self, filename=os.path.join('test_flcompress','test_html_file.html')):
        hf = HuffFile()
        with open(filename, "r") as f:
            BEFORE = f.read()

        dir_name = hf.compress_file(filename)
        filename = os.path.join(dir_name, os.path.split(filename)[1])
        hf.decompress_file(filename + COMPRESSED_FILE_EXTENSION)

        with open(filename, "r") as f:
            AFTER = f.read()

        self.assertEqual(BEFORE, AFTER)

    # test error-handling if file has no contents ~ zero bytes
    def test_flcompress_4(self, filename=os.path.join('test_flcompress','test_zero_text_file.txt')):
        hf = HuffFile()
        with self.assertRaises(CompressionError):
            hf.compress_file(filename) and hf.decompress_file(filename)

    # test error-handling if file is a pdf 
    # (not suitable for compression with this tool)
    def test_flcompress_5(self, filename=os.path.join('test_flcompress','test_incorrect_file_type_1.pdf')):
        hf = HuffFile()
        with self.assertRaises(CompressionError):
            hf.compress_file(filename) and hf.decompress_file(filename)

    # test error-handling if file is an image 
    # (not suitable for compression with this tool)
    def test_flcompress_6(self, filename=os.path.join('test_flcompress','test_incorrect_file_type_2.jpg')):
        hf = HuffFile()
        with self.assertRaises(CompressionError):
            hf.compress_file(filename) and hf.decompress_file(filename)

    # test error-handling if file is an excel file 
    # (not suitable for compression with this tool)
    def test_flcompress_7(self, filename=os.path.join('test_flcompress','test_incorrect_file_type_3.xls')): 
        hf = HuffFile()
        with self.assertRaises(CompressionError):
            hf.compress_file(filename) and hf.decompress_file(filename)

    # test error-handling if compress_file and decompress_file are given 
    # incorrect file types
    def test_flcompress_8(self, filename=os.path.join('test_flcompress','test_small_file.txt')): 
        hf = HuffFile() 
        with self.assertRaises(CompressionError):
            hf.compress_file(filename+COMPRESSED_FILE_EXTENSION)
        with self.assertRaises(CompressionError): 
            hf.decompress_file(filename)


if __name__ == "__main__":
    unittest.main()