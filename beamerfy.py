#!/usr/bin/python3

from beamerfycore import commandparser
from beamerfycore import parser

if __name__ == "__main__":
    commands  = commandparser.CommandParser()

    texparser = parser.Parser(
        commands.arguments.tex_file
    )

    prebeamer = texparser.parsetex()

