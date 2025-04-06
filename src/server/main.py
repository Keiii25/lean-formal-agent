import crewai_tools
import uvicorn
from qdrant_client import QdrantClient
from os import environ, getenv
from dotenv import load_dotenv

from ..tools.math_solver import MathSolverTool
# from ..tools.stock import (
#     FundamentalAnalysis,
#     TechnicalAnalysis,
#     RiskAssessment,
# )
# from ..tools.mindshare_tool import MindshareTool

load_dotenv()

from .api import create_api
from .registry import Registry
# from ..tools.agentipy_tools import gen_tools

# Configure OpenRouter and LiteLLM
environ["OPENAI_API_KEY"] = getenv("OPENAI_API_KEY")  # Make sure this is actually set in your .env or shell
environ["OPENAI_API_BASE"] = "https://api.openai.com/v1"  # ✅ OpenAI official endpoint
environ.pop("OPENAI_API_VERSION", None)  # Optional: unset if not needed
environ.pop("OPENAI_ORGANIZATION", None) 

# Add headers required by OpenRouter
environ["OPENAI_HEADERS"] = '{"HTTP-Referer": "https://agents.vistara.dev", "X-Title": "Z Framework"}'
# Configure LiteLLM
import litellm
litellm.set_verbose = True  # Enable debug logging
litellm.drop_params = True  # Prevent API validation errors

def main():
    client = QdrantClient(host=environ["QDRANT_HOST"], port=int(environ["QDRANT_PORT"]), api_key=environ["QDRANT_API_KEY"])

    registry = Registry(client)

    # TODO this will be made dynamic in the future where tools will be
    # run as their own services
    registry.register_tool("SerperDevTool", crewai_tools.SerperDevTool())
    # registry.register_tool("FundamentalAnalysis", FundamentalAnalysis())
    # registry.register_tool("TechnicalAnalysis", TechnicalAnalysis())
    # registry.register_tool("RiskAssessment", RiskAssessment())
    # registry.register_tool("MindshareTool", MindshareTool())
    registry.register_tool("MathSolverTool", MathSolverTool())
    # for tool_name, tool in gen_tools():
    #     registry.register_tool(tool_name, tool)

    uvicorn.run(create_api(registry), host="0.0.0.0", port=8000)


main()
