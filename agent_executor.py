# agent.py (Logic Corrected)

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the tools directly. The @tool decorator has already prepared them.
from apps.tools.tools import (
    extract_skills_from_text,
    search_for_jobs,
    get_market_insights,
    analyze_resume_against_job,
)

# 1. Define the list of tools by simply listing the imported functions.
tools = [
    extract_skills_from_text,
    search_for_jobs,
    get_market_insights,
    analyze_resume_against_job,
]

# 2. Set up the LLM with the API Key
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"), # Ensure this matches your .env file
    temperature=0,
    convert_system_message_to_human=True
)

# 3. Create the prompt template (with improved logic)
prompt_template = """
You are a comprehensive, multi-tool job search assistant. Your goal is to help users with every step of the job application process.

**CORE INSTRUCTIONS:**
1.  **Understand Intent:** First, determine the user's primary goal. Are they searching for jobs, analyzing a resume, checking ATS scores, or asking for a full-service match?
2.  **Use Context for Data:** The user's direct `input` (e.g., "optimize my resume") is the COMMAND. The data you need (like the `resume_text` or `job_description`) will often be in the surrounding `context` or `memory`.
3.  **Construct Tool Inputs:** When you call ANY tool, you MUST construct a dictionary for its `input` argument. Find the necessary values from the user's full request to populate the dictionary.

**TOOL USAGE GUIDE:**
-   **For simple job searches:** Use `search_for_jobs`.
-   **To compare a resume to a single job:** Use `analyze_resume_against_job`.
-   **To get salary/skill trends:** Use `get_market_insights`.
-   **To improve a resume for one specific job:** Use `optimize_resume_for_job`.
-   **To check a resume's compatibility with automated systems:** Use `ats_check_resume`.
-   **For a complete, end-to-end service (find jobs, rank them, and optimize resumes for the top matches):** Use the powerful `match_jobs_to_resume` tool. This is often the best choice if the user provides a resume and general preferences.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", prompt_template),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 4. Create the Agent
agent = create_tool_calling_agent(llm, tools, prompt)

# 5. Create the Agent Executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
