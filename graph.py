# File: C:\AI_src\marketing-assistant\graph.py

import os
import json
import logging
import re
from typing import TypedDict, Any, List
from pydantic import BaseModel, ValidationError
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

# ─── Environment Setup ─────────────────────────────────────────────────────────
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not set")

BASE_DIR = os.path.dirname(__file__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ─── Load Prompt Content ───────────────────────────────────────────────────────
with open(os.path.join(BASE_DIR, "prompts/agent_1.json"), encoding="utf-8") as f:
    agent1_prompt = json.load(f)
with open(os.path.join(BASE_DIR, "prompts/agent_2.json"), encoding="utf-8") as f:
    agent2_prompt = json.load(f)
with open(os.path.join(BASE_DIR, "knowledge_base/LGarchitect_tools_slim.txt"), encoding="utf-8") as f:
    tools_kb = f.read()
with open(os.path.join(BASE_DIR, "knowledge_base/LGarchitect_multi_agent_slim.txt"), encoding="utf-8") as f:
    multi_kb = f.read()
with open(os.path.join(BASE_DIR, "knowledge_base/LGarchitect_LangGraph_core_slim.txt"), encoding="utf-8") as f:
    core_kb = f.read()

# ─── Data Models ───────────────────────────────────────────────────────────────
class ClientIntake(BaseModel):
    ClientProfile: dict
    SalesOps: dict
    Marketing: dict
    Retention: dict
    AIReadiness: dict
    TechStack: dict
    GoalsTimeline: dict
    HAF: dict
    CII: dict
    ReferenceDocs: str

class IntakeSummary(BaseModel):
    ClientProfile: dict
    Good: List[str]
    Bad: List[str]
    Ugly: List[str]
    SolutionSummary: str
    WorkflowOutline: List[str]
    HAF: dict
    CII: dict

class ClientFacingReport(BaseModel):
    report_markdown: str

class DevFacingReport(BaseModel):
    blueprint_graph: str

class GraphState(TypedDict):
    intake: ClientIntake
    summary: IntakeSummary
    client_report: ClientFacingReport
    dev_report: DevFacingReport

# ─── LLM Init ───────────────────────────────────────────────────────────────────
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.7,
    openai_api_key=OPENAI_API_KEY,
)

# ─── Nodes ─────────────────────────────────────────────────────────────────────
def bootstrap_node(state: GraphState) -> dict:
    logger.info("[BOOTSTRAP] Intake acknowledged.")
    return {}

def summarizer_node(state: GraphState) -> dict:
    raw_json = json.dumps(state["intake"].model_dump(), indent=2)
    messages = [
        SystemMessage(content=agent1_prompt["system"] + "\n\n" + multi_kb),
        HumanMessage(content=agent1_prompt["user_template"].replace("{RAW_INTAKE_JSON}", raw_json))
    ]
    response = llm.invoke(messages)
    try:
        content = response.content.strip()
        if content.startswith("```"):
            content = "\n".join(line for line in content.splitlines() if not line.strip().startswith("```")).strip()
        summary = IntakeSummary.parse_raw(content)
        return {"summary": summary}
    except ValidationError as e:
        logger.error(f"[SUMMARIZER] Validation failed: {e}")
        raise

def report_node(state: GraphState) -> dict:
    summary_json = json.dumps(state["summary"].model_dump(), indent=2)
    messages = [
        SystemMessage(content=agent2_prompt["system"] + "\n\n" + core_kb + "\n" + tools_kb),
        HumanMessage(content=summary_json)
    ]
    response = llm.invoke(messages)
    try:
        content = response.content.strip()
        if content.startswith("```"):
            content = "\n".join(line for line in content.splitlines() if not line.strip().startswith("```")).strip()
        data = json.loads(content)
        return {
            "client_report": ClientFacingReport(report_markdown=data.get("client_report", "")),
            "dev_report": DevFacingReport(blueprint_graph=data.get("developer_report", ""))
        }
    except (json.JSONDecodeError, ValidationError) as e:
        logger.error(f"[REPORT] Parsing failed: {e}")
        raise

# ─── Build Graph ───────────────────────────────────────────────────────────────
builder = StateGraph(GraphState)
builder.add_node("bootstrap", bootstrap_node)
builder.add_node("summarize", summarizer_node)
builder.add_node("report", report_node)
builder.add_edge(START, "bootstrap")
builder.add_edge("bootstrap", "summarize")
builder.add_edge("summarize", "report")
builder.add_edge("report", END)

graph = builder.compile()

# ─── Public API ─────────────────────────────────────────────────────────────────
def run_pipeline(raw_intake: dict) -> Any:
    intake_model = ClientIntake(**raw_intake)
    result = graph.invoke({"intake": intake_model})
    return {
        "client_report": result["client_report"].report_markdown,
        "dev_report": result["dev_report"].blueprint_graph
    }

# ─── Dev Test Hook ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_file = os.path.join(BASE_DIR, "sample_intake.json")
    with open(test_file, encoding="utf-8") as f:
        sample = json.load(f)
    out = run_pipeline(sample)
    print("\n==== CLIENT REPORT ====")
    print(out["client_report"])
    print("\n==== DEV REPORT ====")
    print(out["dev_report"])
