import sympy as sp
from pydantic import BaseModel, Field
from typing import Type
from crewai.tools import BaseTool

class MathSolverSchema(BaseModel):
    problem: str = Field(..., description="The math problem to solve")

class MathSolverTool(BaseTool):
    name: str = "Math Solver"
    description: str = "Solves symbolic math problems including equations, integrals, derivatives, and simplifications."
    args_schema: Type[BaseModel] = MathSolverSchema

    def _run(self, **kwargs):
        problem = kwargs['problem']
        # t = kwargs['problem']
        # print(type(problem))
        # print(type(t))
        # print(t)
        try:
            # Parse and evaluate using SymPy
            x = sp.symbols('x')
            result = eval(f"sp.{problem}")
            return str(result)
        except Exception as e:
            return f"Error solving problem: {str(e)}"
