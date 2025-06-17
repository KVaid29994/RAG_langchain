from langchain.tools import BaseTool
from typing import Type
from pydantic import Field, BaseModel

class MultiplyInput(BaseModel):
    a: int = Field(required = True, description="the first number to multiply")
    b: int = Field(required = True, description="the second number to multiply")

class MultiplyTool(BaseTool):
    name : str = "multiply"
    description : str = "multiply 2 numbers"

    args_schema :  Type[BaseModel] = MultiplyInput

    def _run(self, a:int, b:int) -> int:
        return a*b


multiply_tool = MultiplyTool()

result = multiply_tool.invoke({'a':4, 'b':10})

print (result)
print(multiply_tool.name)