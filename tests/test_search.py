import unittest
import os
from img_decomposition.search import search_for_products

class TestSearchForProducts(unittest.TestCase):
    def test_search_for_products(self):
        image_file_path = os.path.join(os.getcwd(), 'sofa.png')
        result = search_for_products([image_file_path])
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

if __name__ == '__main__':
    unittest.main()
