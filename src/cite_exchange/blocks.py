from pydantic import BaseModel #, Field
import requests

def labels(s: str) -> list[str]:
    """Find the labels in a CEX-formatted string.
    
    Args:
        s (str): A string containing CEX-formatted text."""
    label_set = set()
    for line in s.split('\n'):
        if line.startswith('#!'):
            label = line[2:]  # Remove leading '#!'
            label_set.add(label)
    return sorted(list(label_set))


def valid_label(label: str) -> bool:
    """Check if a label is valid according to CEX format rules.
    
    Args:
        label (str): The label to check, without leading `!#`.
    """
    validlabels = [
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
    return label in validlabels




class CexBlock(BaseModel):
    """A labelled block of text lines.
    
    ADD DETAILS ON CEX FORMAT HERE.

    Attributes:
        label (str): The label of the block, without leading `!#`.
        data (list[str]): The lines of raw text in the block, omitting empty lines and comments.
    
    """
    label: str
    data: list[str]


    @classmethod
    def from_text(cls, src: str, label: str = None) -> list["CexBlock"]:
        """Create a list of `CexBlock`s from a CEX-formatted string source.
        
        Parses CEX format where blocks begin with label lines (starting with `#!`).
        Data lines are non-empty lines that don't start with `//` (comments).
        Multiple blocks can have the same label.
        
        Args:
            src (str): The CEX-formatted text to parse.
            label (str, optional): If provided, only return blocks with this label.
        
        Returns:
            list["CexBlock"]: A list of CexBlock instances, one for each labeled block.
                If label is specified, only blocks matching that label are returned.
        """
        blocks = []
        current_label = None
        current_data = []
        
        for line in src.split('\n'):
            if line.startswith('#!'):
                # Save previous block if it exists
                if current_label is not None and current_data:
                    blocks.append(cls(label=current_label, data=current_data))
                # Start new block
                current_label = line[2:]  # Remove leading '#!'
                current_data = []
            else:
                # Check if this is a valid data line (non-empty, not a comment)
                if current_label is not None and line and not line.startswith('//'):
                    current_data.append(line)
        
        # Don't forget the last block
        if current_label is not None and current_data:
            blocks.append(cls(label=current_label, data=current_data))
        
        # Filter by label if specified
        if label is not None:
            blocks = [b for b in blocks if b.label == label]
        
        return blocks

    @classmethod
    def from_file(cls, filepath: str, label: str = None) -> list["CexBlock"]:
        """Create a list of `CexBlock`s from a CEX-formatted file.
        
        Reads a CEX file and parses it into CexBlock instances. Works identically
        to from_text but reads from a file path instead of a string.
        
        Args:
            filepath (str): Path to the CEX file to parse.
            label (str, optional): If provided, only return blocks with this label.
        
        Returns:
            list["CexBlock"]: A list of CexBlock instances, one for each labeled block.
                If label is specified, only blocks matching that label are returned.
        """
        with open(filepath, 'r') as f:
            content = f.read()
        return cls.from_text(content, label=label)

    @classmethod
    def from_url(cls, url: str, label: str = None) -> list["CexBlock"]:
        """Create a list of `CexBlock`s from a CEX-formatted URL.
        
        Fetches CEX data from a URL and parses it into CexBlock instances. Works identically
        to from_text but retrieves content from a URL instead of a string.
        
        Args:
            url (str): URL pointing to the CEX file to parse.
            label (str, optional): If provided, only return blocks with this label.
        
        Returns:
            list["CexBlock"]: A list of CexBlock instances, one for each labeled block.
                If label is specified, only blocks matching that label are returned.
        """
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return cls.from_text(response.text, label=label)
    