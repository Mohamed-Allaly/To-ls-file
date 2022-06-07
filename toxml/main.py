from xml.dom.minidom import parseString
import  sys, ast, os


class ShowStrings(ast.NodeVisitor):
    def __init__(self, file_ui_path):
        self.file_ui_path = file_ui_path
        self.f = open(self.file_ui_path, 'w+')
        self.dom = parseString('''<?xml version="1.0" encoding="utf-8"?>
            <!DOCTYPE TS>
            <TS version="2.1" language="fr" sourcelanguage="en">
            <context>
            </context>
            </TS>''')
    
    def toxml(self, dom, filename, line, sourceContent):
        context =  dom.getElementsByTagName("context")[0]
        message = dom.createElement("message")
        location = dom.createElement("location")
        location.setAttribute("filename", filename)
        location.setAttribute("line", line)
        source = dom.createElement("source")
        text = dom.createTextNode(sourceContent)
        source.appendChild(text)
        translation = dom.createElement("translation")
        message.appendChild(location)
        message.appendChild(source)
        message.appendChild(translation)
        context.appendChild(message)
        
    def visit_Str(self, node):
        self.toxml(self.dom, "filename/gggggg/tttt", str(node.lineno), str(node.s).replace("'", "'").replace('"', '"'))
    
def parse(file_py_path, file_out_path):
   with open(file_py_path) as f:
       root = ast.parse(f.read())
       show_strings = ShowStrings(file_out_path)
       show_strings.visit(root)
       show_strings.f.write(show_strings.dom.toprettyxml())
       show_strings.f.close()

if __name__ == "__main__":
    try:
        file_in_path = sys.argv[1]
        file_out_path = sys.argv[2]
        parse(file_in_path, file_out_path)
    except Exception as e:
            print(f'\n-------\n{e}\n-------\n')

