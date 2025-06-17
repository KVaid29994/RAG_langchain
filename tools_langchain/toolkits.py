from langchain_core.tools import tool

#custom tools

@tool
def add(a:int, b:int)-> int:
    '''
    Add 2 numbers
    '''
    return a+b

@tool
def multiply(a:int, b:int)-> int:
    '''
    multiply 2 numbers
    '''
    return a*b

class MathTookkit():
    def get_tools(self):
        return [add, multiply]
    
toolkit = MathTookkit()
tools = toolkit.get_tools()

for tool in tools:
    print (tool.name, '=>', tool.description)

