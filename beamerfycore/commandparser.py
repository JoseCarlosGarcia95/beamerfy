import argparse

class CommandParser:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Process beamerfy syntax and genereate a beamer from your *.tex file')
        parser.add_argument('tex_file', help='The file that you want to process')
        parser.add_argument('output_folder', help='The folder where you want to ouput everything.')
        parser.add_argument('--template', nargs='?', default='default', help='Your template')
        
        self.arguments = parser.parse_args()


