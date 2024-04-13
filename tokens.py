"""
This module contains the tokens used by the web2book CLI app. These tokens have
information like the format of the sections, their contents, and whether or not
certain strings are links
"""

from dataclasses import dataclass
from typing import List, Union
from abc import ABC
from enum import Enum
from bs4 import BeautifulSoup, ResultSet

class ElementType(Enum):
    Text=0

@dataclass
class Element:
    el_type: ElementType
    contents: List[ResultSet]

@dataclass
class Section:
    name: str
    elements: List[Element]
    level: int