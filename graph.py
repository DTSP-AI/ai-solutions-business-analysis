import os
import json
import logging
from typing import TypedDict, Any, List
from pydantic import BaseModel, Field, ValidationError
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

# ─── Setup Logging ─────────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%((asctime)s] [%(levelname)s] %(message)s",
)

# ─── Load Environment & Prompts ─────────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY not set in environment!")
    raise EnvironmentError("Missing OPENAI_API_KEY")

BASE_DIR = os.path.dirname(__file__)
with open(os.path.join(BASE_DIR, "prompts/agent_1.json"), "r", encoding="utf-8") as f:
    agent1_prompt = json.load(f)
with open(os.path.join(BASE_DIR, "prompts/agent_2.json"), "r", encoding="utf-8") as f:
    agent2_prompt = json.load(f)
with open(os.path.join(BASE_DIR, "knowledge_base/LGarchitect_tools"), "r", encoding="utf-8") as f:
    kodey_docs = f.read()
with open(os.path.join(BASE_DIR, "knowledge_base/LGarchitect_multi_agent.txt"), "r", encoding="utf-8") as f:
    lg_multi = f.read()
with open(os.path.join(BASE_DIR, "knowledge_base/LGarchitect_LangGraph_core.txt"), "r", encoding="utf-8") as f:
    lg_core = f.read()

# ─── Data Models ────────────────────────────────────────────────────────────────
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
    report_markdown: str = Field(..., description="Markdown text of client-facing report")

class DevFacingReport(BaseModel):
    blueprint_xml: str = Field(..., description="XML/JSON blueprint for implementation")

class GraphState(TypedDict):
    intake: ClientIntake
    summary: IntakeSummary
    client_report: ClientFacingReport
    dev_report: DevFacingReport

# ─── LLM ────────────────────────────────────────────────────────────────────────
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.7,
    openai_api_key=OPENAI_API_KEY,
)

# ─── Node Functions ─────────────────────────────────────────────────────────────
def intake_node(state: GraphState) -> dict:
    logger.info("[📝] Intake node: received raw intake")
    return {}

def summarizer_node(state: GraphState) -> dict:
    logger.info("[🔍] Summarizer node: calling Agent 1")
    raw = state["intake"].json(indent=2)
    system_content = agent1_prompt["system"] + "\n\n" + lg_multi + "\n" + lg_core
    messages = [
        SystemMessage(content=system_content),
        HumanMessage(content=agent1_prompt["user_template"].replace("{RAW_INTAKE_JSON}", raw)),
    ]
    resp = llm(messages)
    try:
        summary = IntakeSummary.parse_raw(resp.content)
    except ValidationError as e:
        logger.error("Summary parsing failed: %s", e)
        raise

    return {"summary": summary}

def report_node(state: GraphState) -> dict:
    logger.info("[📊] Report node: calling Agent 2")
    summary_json = state["summary"].json(indent=2)
    system_content = agent2_prompt["system"] + "\n\n" + lg_multi + "\n" + lg_core
    messages = [
        SystemMessage(content=system_content),
        HumanMessage(content=summary_json),
    ]
    resp = llm(messages)
    try:
        data = json.loads(resp.content)
        client = ClientFacingReport(report_markdown=data.get("client_report", ""))
        dev = DevFacingReport(blueprint_xml=data.get("developer_report", ""))
    except (json.JSONDecodeError, ValidationError) as e:
        logger.error("Report parsing failed: %s", e)
        raise
    return {"client_report": client, "dev_report": dev}

# ─── Build & Compile Graph ──────────────────────────────────────────────────────
builder = StateGraph(GraphState)
builder.add_node("intake", intake_node)
builder.add_node("summarize", summarizer_node)
builder.add_node("report", report_node)

builder.add_edge(START, "intake")
builder.add_edge("intake", "summarize")
builder.add_edge("summarize", "report")
builder.add_edge("report", END)

graph = builder.compile()
logger.info("[✅] Graph compiled successfully")

# ─── Public API ─────────────────────────────────────────────────────────────────
def run_pipeline(raw_intake: dict) -> Any:
    """
    Entry point: run the full graph given a raw intake dict.
    Returns a dict with 'client_report' and 'dev_report'.
    """
    intake_model = ClientIntake(**raw_intake)
    result = graph.invoke({"intake": intake_model}, {})
    return {
        "client_report": result["client_report"].report_markdown,
        "dev_report": result["dev_report"].blueprint_xml,
    }

if __name__ == "__main__":
    sample = json.loads(open(os.path.join(BASE_DIR, "sample_intake.json")).read())
    out = run_pipeline(sample)
    print(out['client_report'])
    print(out['dev_report'])
