# cite_exchange

A Python library for parsing and working with CITE EXchange (CEX) format data.

## Overview

`cite_exchange` provides tools for reading and processing data in CITE EXchange format, a line-oriented text format for managing structured data about scholarly resources. CEX files are organized into labeled blocks, where each block contains tabular data relevant to a specific resource type.

## Installation

```bash
pip install cite_exchange
```

### Requirements
- Python 3.14+
- pydantic >= 2.12.5
- requests (for URL-based parsing)

## Quick Start

```python
from cite_exchange.blocks import CexBlock

# Parse from a string
with open('data.cex', 'r') as f:
    content = f.read()
all_blocks = CexBlock.from_text(content)

# Parse directly from a file
all_blocks = CexBlock.from_file('data.cex')

# Parse directly from a URL
all_blocks = CexBlock.from_url('https://example.com/data.cex')

# Filter by label
ctsdata_blocks = CexBlock.from_file('data.cex', label='ctsdata')

# Access block data
for block in ctsdata_blocks:
    print(f"Label: {block.label}")
    print(f"Data lines: {len(block.data)}")
    for line in block.data:
        print(f"  {line}")
```

## API Reference

### `CexBlock`

A Pydantic model representing a labeled block of text data from a CEX source.

#### Attributes
- `label` (str): The label identifier for this block (without the `#!` prefix)
- `data` (list[str]): List of data lines in this block, excluding empty lines and comments

#### Methods

##### `CexBlock.from_text(src: str, label: str = None) -> list[CexBlock]`

Parse CEX-formatted text and create `CexBlock` instances.

**Parameters:**
- `src` (str): The CEX-formatted text to parse
- `label` (str, optional): If specified, only return blocks matching this label

**Returns:** A list of `CexBlock` instances

**Parsing Rules:**
- Label lines begin with `#!` and define the start of a new block
- Data lines are non-empty and don't start with `//` (comments are ignored)
- Multiple blocks can have the same label type
- Empty lines and comment lines are excluded from block data

**Example:**
```python
# Parse all blocks
blocks = CexBlock.from_text(cex_content)

# Parse only specific label type
catalog_blocks = CexBlock.from_text(cex_content, label='ctscatalog')
```

### Utility Functions

#### `labels(s: str) -> list[str]`

Extract all unique labels from a CEX-formatted string.

**Returns:** Sorted list of unique label names

```python
from cite_exchange.blocks import labels

with open('data.cex', 'r') as f:
    content = f.read()

label_list = labels(content)
print(label_list)  # ['citecollections', 'citedata', 'citeproperties', ...]
```

#### `valid_label(label: str) -> bool`

Check if a label is valid according to CEX format specification.

**Valid labels:**
- cexversion
- citelibrary
- ctsdata
- ctscatalog
- citecollections
- citeproperties
- citedata
- imagedata
- datamodels
- citerelationset
- relationsetcatalog

```python
from cite_exchange.blocks import valid_label

print(valid_label('ctsdata'))    # True
print(valid_label('invalid'))    # False
```

## CEX Format Overview

CEX (CITE EXchange) is a line-oriented format for exchanging data about scholarly resources. Key features:

- **Line-oriented structure**: Data organized into lines and blocks
- **Labeled blocks**: Each block starts with a `#!label` line
- **Tabular data**: Blocks contain pipe-delimited (`|`) or other delimited data
- **Comments**: Lines starting with `//` are comments and ignored
- **Empty lines**: Empty lines are ignored

### Example CEX Content

```
#!ctscatalog
urn|citationScheme|groupName|workTitle
urn:cts:greekLit:tlg0012.tlg001:|book|Homer|Iliad

#!ctsdata
urn:cts:greekLit:tlg0012.tlg001:1.1|Μῆνις ἀ εἴδε θεά
urn:cts:greekLit:tlg0012.tlg001:1.2|Πηληϊάδεω Ἀχιλῆος
```

## Testing

The package includes comprehensive unit tests covering all functionality:

```bash
python -m pytest test/test_blocks.py
```

Test data files are included in `test/data/`:
- `burneysample.cex`: Sample CEX data from the Homer Multitext project
- `laxlibrary1.cex`: Sample CITE collection data

## License

See LICENSE file for details.

## References

- [CITE Architecture](http://www.homermultitext.org/hmt-docs/cite/)
- [Homer Multitext Project](http://www.homermultitext.org/)
