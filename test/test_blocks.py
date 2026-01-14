import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cite_exchange.blocks import labels, valid_label, CexBlock


class TestLabels(unittest.TestCase):
    """Test cases for the labels function."""

    def setUp(self):
        """Load test data."""
        test_data_path = Path(__file__).parent / "data" / "burneysample.cex"
        with open(test_data_path, 'r') as f:
            self.burney_data = f.read()
        
        test_data_path = Path(__file__).parent / "data" / "laxlibrary1.cex"
        with open(test_data_path, 'r') as f:
            self.lax_data = f.read()

    def test_labels_finds_all_labels(self):
        """Test that labels function finds all label lines."""
        result = labels(self.burney_data)
        self.assertIn("ctscatalog", result)
        self.assertIn("ctsdata", result)

    def test_labels_removes_leading_hash_bang(self):
        """Test that leading #! is removed from labels."""
        result = labels(self.burney_data)
        for label in result:
            self.assertFalse(label.startswith("#!"))

    def test_labels_returns_unique_values(self):
        """Test that labels returns unique values only."""
        result = labels(self.burney_data)
        self.assertEqual(len(result), len(set(result)))

    def test_labels_returns_sorted_list(self):
        """Test that labels returns a sorted list."""
        result = labels(self.burney_data)
        self.assertEqual(result, sorted(result))
    
    def test_labels_with_multiple_blocks_same_label(self):
        """Test that labels correctly handles multiple blocks with same label."""
        result = labels(self.lax_data)
        # laxlibrary1.cex has two #!ctsdata blocks, but should only appear once
        self.assertEqual(result.count("ctsdata"), 1)


class TestValidLabel(unittest.TestCase):
    """Test cases for the valid_label function."""

    def test_valid_label_accepts_valid_labels(self):
        """Test that valid_label accepts all valid CEX labels."""
        valid_labels = [
            "cexversion",
            "citelibrary",
            "ctsdata",
            "ctscatalog",
            "citecollections",
            "citeproperties",
            "citedata",
            "imagedata",
            "datamodels",
            "citerelationset",
            "relationsetcatalog"
        ]
        for label in valid_labels:
            self.assertTrue(valid_label(label), f"Expected {label} to be valid")

    def test_valid_label_rejects_invalid_labels(self):
        """Test that valid_label rejects invalid labels."""
        invalid_labels = ["invalid", "foo", "bar", "ctsdata ", " ctsdata", "cts data"]
        for label in invalid_labels:
            self.assertFalse(valid_label(label), f"Expected {label} to be invalid")

    def test_valid_label_rejects_empty_string(self):
        """Test that valid_label rejects empty strings."""
        self.assertFalse(valid_label(""))


class TestCexBlockFromLines(unittest.TestCase):
    """Test cases for the CexBlock.from_text method."""

    def setUp(self):
        """Load test data."""
        test_data_path = Path(__file__).parent / "data" / "burneysample.cex"
        with open(test_data_path, 'r') as f:
            self.burney_data = f.read()
        
        test_data_path = Path(__file__).parent / "data" / "laxlibrary1.cex"
        with open(test_data_path, 'r') as f:
            self.lax_data = f.read()

    def test_from_text_returns_list_of_cex_blocks(self):
        """Test that from_text returns a list of CexBlock objects."""
        result = CexBlock.from_text(self.burney_data)
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(b, CexBlock) for b in result))

    def test_from_text_parses_all_blocks(self):
        """Test that from_text parses all labeled blocks."""
        result = CexBlock.from_text(self.burney_data)
        labels_found = [b.label for b in result]
        self.assertIn("ctscatalog", labels_found)
        self.assertIn("ctsdata", labels_found)

    def test_from_text_excludes_empty_lines(self):
        """Test that from_text excludes empty lines from data."""
        result = CexBlock.from_text(self.burney_data)
        for block in result:
            self.assertTrue(all(line.strip() for line in block.data))

    def test_from_text_excludes_comments(self):
        """Test that from_text excludes comment lines starting with //."""
        result = CexBlock.from_text(self.lax_data)
        for block in result:
            self.assertTrue(all(not line.startswith('//') for line in block.data))

    def test_from_text_filters_by_label(self):
        """Test that from_text filters by label when specified."""
        result = CexBlock.from_text(self.burney_data, label="ctscatalog")
        self.assertTrue(all(b.label == "ctscatalog" for b in result))
        self.assertEqual(len(result), 1)

    def test_from_text_returns_multiple_blocks_same_label(self):
        """Test that from_text handles multiple blocks with same label."""
        result = CexBlock.from_text(self.lax_data, label="ctsdata")
        # laxlibrary1.cex has two #!ctsdata blocks
        self.assertEqual(len(result), 2)
        self.assertTrue(all(b.label == "ctsdata" for b in result))

    def test_from_text_no_blocks_for_invalid_label(self):
        """Test that from_text returns empty list for non-existent label."""
        result = CexBlock.from_text(self.burney_data, label="nonexistent")
        self.assertEqual(result, [])

    def test_from_text_preserves_data_lines(self):
        """Test that from_text preserves the data lines exactly."""
        result = CexBlock.from_text(self.burney_data, label="ctsdata")
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0].data), 3)

    def test_from_text_handles_multiline_data(self):
        """Test that from_text handles blocks with multiple data lines."""
        result = CexBlock.from_text(self.lax_data, label="citecollections")
        self.assertEqual(len(result), 1)
        self.assertGreater(len(result[0].data), 0)

    def test_cex_block_instantiation(self):
        """Test that CexBlock can be instantiated with label and data."""
        block = CexBlock(label="test", data=["line1", "line2"])
        self.assertEqual(block.label, "test")
        self.assertEqual(block.data, ["line1", "line2"])

class TestCexBlockFromFile(unittest.TestCase):
    """Test cases for the CexBlock.from_file method."""

    def setUp(self):
        """Set up paths to test data files."""
        self.burney_file = Path(__file__).parent / "data" / "burneysample.cex"
        self.lax_file = Path(__file__).parent / "data" / "laxlibrary1.cex"

    def test_from_file_returns_list_of_cex_blocks(self):
        """Test that from_file returns a list of CexBlock objects."""
        result = CexBlock.from_file(str(self.burney_file))
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(b, CexBlock) for b in result))

    def test_from_file_parses_all_blocks(self):
        """Test that from_file parses all labeled blocks from file."""
        result = CexBlock.from_file(str(self.burney_file))
        labels_found = [b.label for b in result]
        self.assertIn("ctscatalog", labels_found)
        self.assertIn("ctsdata", labels_found)

    def test_from_file_filters_by_label(self):
        """Test that from_file filters by label when specified."""
        result = CexBlock.from_file(str(self.burney_file), label="ctscatalog")
        self.assertTrue(all(b.label == "ctscatalog" for b in result))
        self.assertEqual(len(result), 1)

    def test_from_file_handles_multiple_blocks_same_label(self):
        """Test that from_file handles multiple blocks with same label from file."""
        result = CexBlock.from_file(str(self.lax_file), label="ctsdata")
        # laxlibrary1.cex has two #!ctsdata blocks
        self.assertEqual(len(result), 2)
        self.assertTrue(all(b.label == "ctsdata" for b in result))

    def test_from_file_no_blocks_for_invalid_label(self):
        """Test that from_file returns empty list for non-existent label."""
        result = CexBlock.from_file(str(self.burney_file), label="nonexistent")
        self.assertEqual(result, [])

    def test_from_file_preserves_data_lines(self):
        """Test that from_file preserves the data lines exactly."""
        result = CexBlock.from_file(str(self.burney_file), label="ctsdata")
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0].data), 3)

    def test_from_file_excludes_comments(self):
        """Test that from_file excludes comment lines starting with //."""
        result = CexBlock.from_file(str(self.lax_file))
        for block in result:
            self.assertTrue(all(not line.startswith('//') for line in block.data))

    def test_from_file_excludes_empty_lines(self):
        """Test that from_file excludes empty lines from data."""
        result = CexBlock.from_file(str(self.lax_file))
        for block in result:
            self.assertTrue(all(line.strip() for line in block.data))

    def test_from_file_nonexistent_file(self):
        """Test that from_file raises an error for nonexistent files."""
        with self.assertRaises(FileNotFoundError):
            CexBlock.from_file("/nonexistent/path/file.cex")


class TestCexBlockFromUrl(unittest.TestCase):
    """Test cases for the CexBlock.from_url method."""

    def setUp(self):
        """Load test data for mocking."""
        test_data_path = Path(__file__).parent / "data" / "burneysample.cex"
        with open(test_data_path, 'r') as f:
            self.burney_data = f.read()
        
        test_data_path = Path(__file__).parent / "data" / "laxlibrary1.cex"
        with open(test_data_path, 'r') as f:
            self.lax_data = f.read()

    @patch('cite_exchange.blocks.requests.get')
    def test_from_url_returns_list_of_cex_blocks(self, mock_get):
        """Test that from_url returns a list of CexBlock objects."""
        mock_response = MagicMock()
        mock_response.text = self.burney_data
        mock_get.return_value = mock_response
        
        result = CexBlock.from_url("https://example.com/data.cex")
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(b, CexBlock) for b in result))

    @patch('cite_exchange.blocks.requests.get')
    def test_from_url_parses_all_blocks(self, mock_get):
        """Test that from_url parses all labeled blocks from URL."""
        mock_response = MagicMock()
        mock_response.text = self.burney_data
        mock_get.return_value = mock_response
        
        result = CexBlock.from_url("https://example.com/data.cex")
        labels_found = [b.label for b in result]
        self.assertIn("ctscatalog", labels_found)
        self.assertIn("ctsdata", labels_found)

    @patch('cite_exchange.blocks.requests.get')
    def test_from_url_filters_by_label(self, mock_get):
        """Test that from_url filters by label when specified."""
        mock_response = MagicMock()
        mock_response.text = self.burney_data
        mock_get.return_value = mock_response
        
        result = CexBlock.from_url("https://example.com/data.cex", label="ctscatalog")
        self.assertTrue(all(b.label == "ctscatalog" for b in result))
        self.assertEqual(len(result), 1)

    @patch('cite_exchange.blocks.requests.get')
    def test_from_url_handles_multiple_blocks_same_label(self, mock_get):
        """Test that from_url handles multiple blocks with same label from URL."""
        mock_response = MagicMock()
        mock_response.text = self.lax_data
        mock_get.return_value = mock_response
        
        result = CexBlock.from_url("https://example.com/data.cex", label="ctsdata")
        self.assertEqual(len(result), 2)
        self.assertTrue(all(b.label == "ctsdata" for b in result))

    @patch('cite_exchange.blocks.requests.get')
    def test_from_url_no_blocks_for_invalid_label(self, mock_get):
        """Test that from_url returns empty list for non-existent label."""
        mock_response = MagicMock()
        mock_response.text = self.burney_data
        mock_get.return_value = mock_response
        
        result = CexBlock.from_url("https://example.com/data.cex", label="nonexistent")
        self.assertEqual(result, [])

    @patch('cite_exchange.blocks.requests.get')
    def test_from_url_excludes_comments(self, mock_get):
        """Test that from_url excludes comment lines starting with //."""
        mock_response = MagicMock()
        mock_response.text = self.lax_data
        mock_get.return_value = mock_response
        
        result = CexBlock.from_url("https://example.com/data.cex")
        for block in result:
            self.assertTrue(all(not line.startswith('//') for line in block.data))

    @patch('cite_exchange.blocks.requests.get')
    def test_from_url_excludes_empty_lines(self, mock_get):
        """Test that from_url excludes empty lines from data."""
        mock_response = MagicMock()
        mock_response.text = self.lax_data
        mock_get.return_value = mock_response
        
        result = CexBlock.from_url("https://example.com/data.cex")
        for block in result:
            self.assertTrue(all(line.strip() for line in block.data))

    @patch('cite_exchange.blocks.requests.get')
    def test_from_url_calls_requests_get_with_url(self, mock_get):
        """Test that from_url calls requests.get with the correct URL."""
        mock_response = MagicMock()
        mock_response.text = self.burney_data
        mock_get.return_value = mock_response
        
        url = "https://example.com/data.cex"
        CexBlock.from_url(url)
        mock_get.assert_called_once_with(url)

    @patch('cite_exchange.blocks.requests.get')
    def test_from_url_raises_for_bad_status(self, mock_get):
        """Test that from_url raises an exception for bad HTTP status codes."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        mock_get.return_value = mock_response
        
        with self.assertRaises(Exception):
            CexBlock.from_url("https://example.com/nonexistent.cex")

    def test_from_url_with_real_url(self):
        """Test that from_url works with a real HMT CEX file."""
        url = "https://raw.githubusercontent.com/homermultitext/hmt-archive/refs/heads/master/releases-cex/hmt-2024c.cex"
        
        try:
            result = CexBlock.from_url(url)
            # Verify result is a list of CexBlocks
            self.assertIsInstance(result, list)
            self.assertTrue(all(isinstance(b, CexBlock) for b in result))
            # Verify we got some blocks
            self.assertGreater(len(result), 0)
            # Verify blocks have the expected structure
            for block in result:
                self.assertIsInstance(block.label, str)
                self.assertIsInstance(block.data, list)
        except Exception as e:
            # Skip this test if network is unavailable
            self.skipTest(f"Network unavailable or URL inaccessible: {e}")


if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    unittest.main()