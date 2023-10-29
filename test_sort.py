import unittest
import sort
from pathlib import Path
class TestSort(unittest.TestCase):
    def test_sort_name(self):
        this_directory = Path.cwd()
        return_value = sort.sort_name(this_directory, "main.py")
        return_value = [value.name for value in return_value]
        self.assertEqual(return_value, ["main.py"])
    
    def test_sort_date(self):
        this_directory = Path.cwd()
        date = {
            "day": 1,
            "month": 8,
            "year": 2023
        }
        return_value = sort.sort_date(this_directory, date)
        return_value = [value.name for value in return_value]
        self.assertIn("date.txt", return_value)

    def test_type(self):
        this_directory = Path.cwd()
        return_value = sort.sort_type(this_directory, ".txt")
        return_value = [value.name for value in return_value]
        self.assertEqual(["date.txt"], return_value)

    def test_group_sort_type(self):
        this_directory = Path.cwd() / "test group"
        return_value = len(sort.sort_all_type(this_directory).keys())
        self.assertEqual(return_value, 2)
    
    def test_group_sort_date(self):
        this_directory = Path.cwd() / "test group"
        return_value = len(sort.sort_all_date(this_directory).keys())
        self.assertEqual(return_value, 2)
    
    def test_create_move_files(self):
        this_directory = Path.cwd() / "test group"
        return_value = len(sort.sort_all_date(this_directory).keys())
        self.assertEqual(return_value, 2)


if __name__ == "__main__":
    unittest.main()