import unittest
import os
import pandas as pd
from excentus_main import generate_path, generate_output_path, create_visualization  # Replace `excentus_main` with your actual script name

class TestFunctions(unittest.TestCase):

    def test_generate_path(self):
        # Test the path generation for a file
        result = generate_path("test_file.xlsx")
        expected = os.path.join(".", "data", "test_file.xlsx")
        self.assertEqual(result, expected)

    def test_generate_output_path(self):
        # Test the path generation for an output file
        result = generate_output_path("output_file.xlsx")
        expected = os.path.join(".", "output_data", "output_file.xlsx")
        self.assertEqual(result, expected)
        self.assertTrue(os.path.exists(os.path.dirname(result)))  # Check if the directory is created

    def test_create_visualization(self):
        # Test the visualization creation function
        # Prepare a sample dataframe
        data = {
            'Customer Name': ['Customer A', 'Customer B'],
            'Total Receivable': [1000, 1500]
        }
        df = pd.DataFrame(data)
        
        # Run the function (it should create a file in the output directory)
        create_visualization(df)
        
        # Check if the file is created
        output_file = os.path.join(".", "output_data", "Total_Receivable_by_Customer.png")
        self.assertTrue(os.path.exists(output_file))

if __name__ == "__main__":
    unittest.main()
