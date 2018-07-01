import os

def readtemplate(template):
    templateinfo = {}
    templatepath = os.getenv("HOME") + "/.beamerfy/templates/" + template + ".tex"

    if not os.path.exists(templatepath):
        raise Exception('Template not found.', 'Unable to found ' + template)

    templateinfo['output'] = open(templatepath).read()

    return templateinfo

def beamergenerate(template, prebeamer):
    beamerdata = ''

    mytemplate = readtemplate(template)

    insideframe = False
    insideitemize = False

    index         = 0

    title         = ''
    author        = ''
    
    for prebeameritem in prebeamer:
        if prebeameritem['command'] == 'new-frame':

            if insideitemize:
                beamerdata += r'\end{itemize}' + "\n"
            if insideframe:
                beamerdata += r'\end{frame}' + "\n"

            beamerdata += r'\begin{frame}' + "\n"
            beamerdata += r'\frametitle{' + prebeameritem['title_frame'] + '}' + "\n"

            insideframe   = True
            insideitemize = False
        elif prebeameritem['command'] == 'beamer-author':
            author        = prebeameritem['author']
        elif prebeameritem['command'] == 'beamer-title':
            title         = prebeameritem['title']
        elif prebeameritem['command'] == 'frame-item':
            if not insideitemize:
                beamerdata += r'\begin{itemize}' + "\n"

            beamerdata += r'\item ' + prebeameritem['frame_item'] + "\n"

            insideitemize = True

        elif prebeameritem['command'] == 'start-raw':
            if insideitemize:
                beamerdata += r'\end{itemize}' + "\n"
            
            prebeamercopy = list(prebeamer)
            prebeamercopy = prebeamercopy[index + 1:]

            nextendraw    = None
            for prebeamercopyitem in prebeamercopy:
                if prebeamercopyitem['command'] == 'end-raw':
                    nextendraw = prebeamercopyitem
                    break

            if nextendraw == None:
                raise Exception('Unable to find end-raw.', 'End-raw neccesary.')

            with open(prebeameritem['file']) as file:
                lines = file.readlines()
                rawlines = lines[prebeameritem['line'] + 1:nextendraw['line']]

                beamerdata += "\n".join(rawlines)

            insideitemize = False

        index += 1
            
    if insideitemize:
        beamerdata += r'\end{itemize}' + "\n"
    if insideframe:
        beamerdata += r'\end{frame}' + "\n"

    
    return mytemplate['output'].replace('%beamer-data', beamerdata).replace('%beamer-author', author).replace('%beamer-title', title)