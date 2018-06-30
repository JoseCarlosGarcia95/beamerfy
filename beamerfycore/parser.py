import os

class Parser:
    def __init__(self, tex_file):
        if not os.path.exists(tex_file):
            raise Exception("Invalid tex file", "{} does not exists!".format(tex_file))
        
        self.tex_file   = os.path.realpath(tex_file)
        self.tex_folder = os.path.dirname(self.tex_file)

    def parsetex(self):
        prebeamer = []
        with open(self.tex_file) as file:
            lines = file.readlines()

            index = 0
            for line in lines:
                line = line.strip()
                
                if line.startswith("%beamerfy:"):
                    beamerfy_syntax = line[len("%beamerfy:"):].strip()
                    beamerfy_dict   = {}
                    
                    command         = beamerfy_syntax.split(' ')[0]

                    if command == "new-frame":
                        beamerfy_dict["command"]     = command
                        beamerfy_dict["title_frame"] = beamerfy_syntax[len(command):].strip()
                    elif command == "frame-item":
                        beamerfy_dict["command"]     = command
                        beamerfy_dict["frame_item"]  = beamerfy_syntax[len(command):].strip()
                    elif command == "start-raw" or command == "end-raw":
                        beamerfy_dict["command"]     = command
                        beamerfy_dict["line"]        = index
                        beamerfy_dict["file"]        = self.tex_file
                    elif command == "new-image":
                        beamerfy_dict["command"]     = command
                        items                        = beamerfy_syntax.split(' ')

                        if len(items) >= 1:
                            beamerfy_dict["image"]   = items[0]

                        if len(items) >= 2:
                            beamerfy_dict["mode"]    = items[1]
                            
                    else:
                        raise Exception("Unknown command {}".format(command), "On line {} at {}"
                        .format(index, self.tex_file))
                    
                    prebeamer.append(beamerfy_dict)
                elif line.startswith("\input{"):
                    newlatex_file = "{}/{}".format(self.tex_folder, line[len("\input{"):])
                    newlatex_file = newlatex_file[:-1]

                    newparser     = Parser(newlatex_file)
                    prebamer_new  = newparser.parsetex()

                    prebeamer.extend(prebamer_new)

                index = index + 1
        return prebeamer