import logging.config
import typer
from typing_extensions import Annotated
import logging
from rich.logging import RichHandler
import requests
from bs4 import BeautifulSoup

import parsers
import generate

# Set up rich logger
logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)
logger = logging.getLogger("rich")

def main(url: Annotated[str, typer.Argument(help="The URL that contains the documentation home page")], loglevel: str="DEBUG"):
    """
    Welcome to the WebToBook CLI app! 🌎->📖

    This app converts documentation websites into textbook-quality PDFs using a
    custom web parser, an autocoder, and the typst typesetting system.

    It is compatible with many documentation websites, and uses frontend web
    scraping which means you do not need access to the code that was used to
    generate the documentation site. 
    """
    
    # %% Download 
    logger.info( f"Retriving data from {url}" )
    text = requests.get( url ).text

    #%% Run Parser
    logger.debug( f"Setting up parser" )
    page = BeautifulSoup( text, "html.parser" )
    parser = parsers.get_parser( page )
    logger.info( f"Using parser: {parser.name}" )
    output = parser.parse( page )
    
    #%% Run the generator
    book = generate.generate_book( output )
    with open("book.typ", "w") as f:
        f.write( book )
    logger.info(f"Thanks for using WebToBook! 🎉")

#%% 
if __name__ == "__main__":
    typer.run(main)