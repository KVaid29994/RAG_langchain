from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class MultiplyInput(BaseModel):
    a: int = Field(required = True, description="the first number to multiply")
    b: int = Field(required = True, description="the second number to multiply")

def multiply_func(a:int, b:int) -> int:
    ''' Multiply 2 numbers'''
    return a*b

multiply_tool = StructuredTool.from_function(func= multiply_func, name="multiply", args_schema=MultiplyInput)

result = multiply_tool.invoke({"a":3, "b":4})
print(result)
print(multiply_tool.name)
print(multiply_tool.description)
print(multiply_tool.args)