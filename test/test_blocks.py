import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cite_exchange.blocks import labels


class TestLabels(unittest.TestCase):
    """Test cases for the labels function."""

    def setUp(self):
        """Load test data."""
        test_data_path = Path(__file__).parent / "data" / "burneysample.cex"
        with open(test_data_path, 'r') as f:
            self.cex_data = f.read()

    def test_labels_finds_all_labels(self):
        """Test that labels function finds all label lines."""
        result = labels(self.cex_data)
        self.assertIn("ctscatalog", result)
        self.assertIn("ctsdata", result)

    def test_labels_removes_leading_hash_bang(self):
        """Test that leading #! is removed from labels."""
        result = labels(self.cex_data)
        for label in result:
            self.assertFalse(label.startswith("#!"))

    def test_labels_returns_unique_values(self):
        """Test that labels returns unique values only."""
        result = labels(self.cex_data)
        self.assertEqual(len(result), len(set(result)))

    def test_labels_returns_sorted_list(self):
        """Test that labels returns a sorted list."""
        result = labels(self.cex_data)
        self.assertEqual(result, sorted(result))


if __name__ == '__main__':
    unittest.main()
