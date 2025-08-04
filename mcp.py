# mcp.py

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from agent_executor import agent_executor
from langchain_core.runnables import RunnableConfig
import uuid

router = APIRouter()

# --- Request & Response Models ---
class MCPContext(BaseModel):
    session_id: Optional[str] = None
    preferred_tools: Optional[List[str]] = None
    persona: Optional[str] = None
    memory: Optional[Dict[str, Any]] = None

class MCPRequest(BaseModel):
    input: str
    context: Optional[MCPContext] = None

class MCPResponse(BaseModel):
    output: str
    tools_used: List[str]
    session_id: str
    context_updated: Dict[str, Any]

# --- Endpoint ---
@router.post("/mcp/invoke", response_model=MCPResponse)
async def invoke_mcp_agent(payload: MCPRequest):
    try:
        session_id = payload.context.session_id if payload.context and payload.context.session_id else str(uuid.uuid4())

        config = RunnableConfig(
            configurable={
                "session_id": session_id,
                "preferred_tools": payload.context.preferred_tools if payload.context else [],
                "persona": payload.context.persona if payload.context else "",
            }
        )

        result = await agent_executor.ainvoke({
            "input": payload.input
        }, config=config)

        # Optional: Extract tools used (you can track it via callbacks or metadata)
        tools_used = [tool.name for tool in agent_executor.tools]

        return MCPResponse(
            output=result["output"],
            tools_used=tools_used,
            session_id=session_id,
            context_updated={
                "persona": payload.context.persona if payload.context else None,
                "preferred_tools": payload.context.preferred_tools if payload.context else []
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MCP Agent Error: {str(e)}")
