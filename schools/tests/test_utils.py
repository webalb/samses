from django.test import TestCase
import os
import shutil
from datetime import datetime

from schools.utils import remove_old_file

class RemoveOldFileTest(TestCase):

    def setUp(self):
        # Create temporary directories
        # Get current date for directory names
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")

        # Create temporary directories
        self.test_dir = os.path.join(os.path.dirname(__file__), 'test_files') 
        os.makedirs(self.test_dir, exist_ok=True)
        os.makedirs(f"{self.test_dir}/{year}", exist_ok=True)
        os.makedirs(f"{self.test_dir}/{year}/{month}", exist_ok=True)
        os.makedirs(f"{self.test_dir}/{year}/{month}/{day}", exist_ok=True)

        # Create a test file
        self.test_file_path = f"{self.test_dir}/{year}/{month}/{day}/test_file.txt"
        with open(self.test_file_path, 'w') as f:
            f.write("Test file content")

    def tearDown(self):
        """
        Removes the test directory and its contents if it exists.
        """
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    def test_remove_old_file_success(self):
        """Test successful removal of file and empty directories."""
        result = remove_old_file(self.test_file_path)
        self.assertTrue(result)
        self.assertFalse(os.path.exists(self.test_file_path))
        self.assertFalse(os.path.exists(f"{self.test_dir}/year/month/day"))
        self.assertFalse(os.path.exists(f"{self.test_dir}/year/month"))
        self.assertFalse(os.path.exists(f"{self.test_dir}/year"))

    def test_remove_old_file_file_not_found(self):
        """Test handling of file not found."""
        non_existent_file = "non_existent_file.txt"
        result = remove_old_file(non_existent_file)
        self.assertFalse(result)

    def test_remove_old_file_non_empty_directory(self):
        """Test handling of non-empty directories."""
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        self.other_file = f"{self.test_dir}/{year}/{month}/other_file.txt"
        with open(self.other_file, 'w') as f:
            f.write("Another file")

        result = remove_old_file(self.other_file)
        self.assertTrue(result)  # File should be removed successfully
        self.assertTrue(os.path.exists(f"{self.test_dir}/{year}/{month}"))  # Directory should not be removed

    def test_remove_old_file_invalid_path(self):
        """Test handling of invalid file paths."""
        invalid_path = "" 
        result = remove_old_file(invalid_path)
        self.assertFalse(result)