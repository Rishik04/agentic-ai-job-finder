# main.py

from fastapi import FastAPI, HTTPException
from agent_executor import agent_executor
from models import AgentRequest, AgentResponse
from dotenv import load_dotenv
import os
from mcp import router as mcp_router

# Load environment variables from .env file
load_dotenv()

# --- App Initialization ---
app = FastAPI(
    title="LangChain Job Agent Server",
    description="An AI agent that uses an LLM and tools to help with job searching.",
    version="2.0.0"
)

app.include_router(mcp_router)

# Check for API Key on startup
# if not os.getenv("GEMINI_API_KEY"):
#     raise RuntimeError("GEMINI_API_KEY not found in .env file. The server cannot start.")

# --- API Endpoints ---
@app.post("/agent/invoke", response_model=AgentResponse, summary="Invoke the LangChain Agent")
async def invoke_agent(request: AgentRequest):
    """
    Sends a query to the LangChain agent and returns its final response.
    The agent will use its tools to fulfill the request.
    """
    try:
        # The agent executor runs asynchronously and returns the final output
        result = await agent_executor.ainvoke({
            "input": request.query
        })
        return AgentResponse(output=result["output"])
    except Exception as e:
        print(f"An error occurred during agent execution: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/agent/tools", summary="List all available LangChain tools and usage details")
async def list_agent_tools():
    try:
        tool_list = []
        for tool in agent_executor.tools:
            tool_info = {
                "name": tool.name,
                "description": tool.description or "No description provided.",
                "doc": tool.func.__doc__ if hasattr(tool.func, "__doc__") else "",
                "prompt_format": f"{tool.name}(...)",
                "parameters": tool.args or []
            }
            tool_list.append(tool_info)

        return {
            "count": len(tool_list),
            "tools": tool_list
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))