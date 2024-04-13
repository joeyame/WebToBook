from parsers import ParserOutput

def generate_book(parsed: ParserOutput) -> str:
    output = ""
    for section in parsed.contents:
        output += "\n\n" + "="*section.level + " " + section.name
        for element in section.elements:
            output += "\n\n"
            output += "".join([e.text.replace('’', '\'') for e in element.contents])
    return output

# def create_outline(parsed: ParserOutput):
#     for section in parsed.contents:
#         print("#"*section.level+section.name)
#         print([e.contents for e in section.elements])
