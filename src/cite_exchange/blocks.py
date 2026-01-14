from pydantic import BaseModel #, Field

def labels(s: str) -> list[str]:
    """Find the labels in a CEX-formatted string."""
    label_set = set()
    for line in s.split('\n'):
        if line.startswith('#!'):
            label = line[2:]  # Remove leading '#!'
            label_set.add(label)
    return sorted(list(label_set))


class CexBlock(BaseModel):
    """A labelled block of text lines.
    
    ADD DETAILS ON CEX FORMAT HERE.

    Attributes:
        label (str): The label of the block, without leading `!#`.
        data (list[str]): The lines of raw text in the block, omitting empty lines and comments.
    
    """
    label: str
    data: list[str]



    



    def from_lines(src: str, label: str) -> list["CexBlock"]:
        """Create a list of `CexBlock`s from a string source.
        
        
        
        Args:
            src (str): The text to parse into a list of `CexBlock`s.
            label (str): The label of the blocks to retrieve, without leading `!#`.
            """

