"""
A package that contains parsers for various documentation sites. This will allow
each to be handled separately, requiring more work but perhaps making the output
more consistent.
"""

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Union

from tokens import Section


@dataclass
class ParserOutput:
    child_urls: List[str]
    contents: List[Section]

from . import ReadTheDocs

class Parser(ABC):
    """
    A parser for a specific documentation site.
    """

    @abstractmethod
    def parser_applies(soup: BeautifulSoup) -> bool:
        """
        Checks if a webpage should be scraped by the parser
        """
    
    @abstractmethod
    def parse(soup: BeautifulSoup) -> ParserOutput:
        """
        Parses a webpage using this parser
        """

def get_parser(soup: BeautifulSoup) -> Parser:
    """
    Gets the parser for the given soup. Will raise a ValueError if no parser is
    found for the specified site.
    """
    if ReadTheDocs.parser_applies(soup):
        return ReadTheDocs
    else:
        raise ValueError("A parser for this site was not found!")