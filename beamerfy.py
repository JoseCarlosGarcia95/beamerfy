#!/usr/bin/python3
import os

from beamerfycore import commandparser
from beamerfycore import parser
from beamerfycore import beamer_generator
if __name__ == '__main__':
    commands  = commandparser.CommandParser()

    texparser = parser.Parser(
        commands.arguments.tex_file
    )

    prebeamer  = texparser.parsetex()
    beamerdata = beamer_generator.beamergenerate(commands.arguments.template, prebeamer)

    if not os.path.exists(commands.arguments.output_folder):
        os.makedirs(commands.arguments.output_folder)


    outputfile = open(commands.arguments.output_folder + "/beamerfy_result.tex", 'w')
    outputfile.write(beamerdata)
    outputfile.close()
