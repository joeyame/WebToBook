"""
A parser for Read the Docs documentation sites.
"""

# Spyder setup commands
# import requests
# url = "https://rich.readthedocs.io/en/stable/logging.html"
# html = requests.get(url)
# soup = BeautifulSoup(html.text, "html.parser")

from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Union
from abc import ABC
import re
from enum import Enum
import logging
logger = logging.getLogger("rich")

from . import ParserOutput
from tokens import ElementType, Element, Section

name = "Read the Docs"

def parser_applies(soup: BeautifulSoup) -> bool:
    """
    Checks if a webpage should be scraped by the readthedocs parser
    """
    return "READTHEDOCS_DATA" in str(soup)

def parse(soup: BeautifulSoup) -> ParserOutput:
    output = ParserOutput([], [])
    
    body = soup.find(itemprop="articleBody")
    sections = body.find_all("section", recursive=False)
    for section in sections:
        output.contents.extend(
            scan_sections( section )
        )
    return output

def scan_sections(section: BeautifulSoup, level=1) -> List[Section]:
    output = []
    
    children = section.find_all(recursive=False)
    elements = []
    name = children.pop(0).text[:-1]
    for child in children:
        if child.name == 'section':
            output.extend( scan_sections( child, level+1 ) )
        elif child.name == 'p':
            elements.append(
                Element(
                    ElementType.Text,
                    contents=list(child.children)
                )
            )
        else:
            logger.warning(f"Unable to parse element: {child.name}")
            
    output.insert(0, Section(
        name,
        elements,
        level
        )
    )

    return output

def create_outline(parsed: ParserOutput):
    for section in parsed.contents:
        print("#"*section.level+section.name)
        print([e.contents for e in section.elements])