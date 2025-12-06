"""
LangGraph-based workflow orchestration for extraction pipeline.

This module implements a state-based graph workflow that:
1. Lists all markdown files from MinIO
2. Fetches each markdown file
3. Extracts company information using LangExtract
4. Saves results as JSON back to MinIO
"""

from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from src.modules.minio_manager import MinIOManager
from src.agents.about_extractor import AboutExtractor
from src.models.schemas import CompanyInfoLite


class ScrapeState(TypedDict, total=False):
    """
    State definition for the extraction workflow.
    """

    objects: List[str]  # List of markdown object names
    index: int  # Current processing index
    current_object: Optional[str]  # Current object being processed
    markdown: Optional[str]  # Current markdown content
    company_info: Optional[CompanyInfoLite]  # Extracted company info
    stats: dict  # Processing statistics


# Initialize global instances
minio_mgr = MinIOManager()
extractor = AboutExtractor()


def node_list_objects(state: ScrapeState) -> ScrapeState:
    """
    Node 1: List all markdown files from MinIO.
    """
    print("📁 Listing markdown files from MinIO...")

    objs = minio_mgr.list_objects(prefix="scraped-content/", recursive=False, limit=20)
    md_objects = [o["object_name"] for o in objs if o["object_name"].endswith(".md")]

    print(f"✓ Found {len(md_objects)} markdown files")

    return {
        **state,
        "objects": md_objects,
        "index": 0,
        "stats": {"total": len(md_objects), "success": 0, "skipped": 0, "errors": 0},
    }


def node_fetch_markdown(state: ScrapeState) -> ScrapeState:
    """
    Node 2: Fetch markdown content for current object.
    """
    objects = state.get("objects", [])
    idx = state.get("index", 0)

    if idx >= len(objects):
        return state  # No more objects to process

    obj_name = objects[idx]
    print(f"\n[{idx + 1}/{len(objects)}] Processing: {obj_name}")

    # Check if JSON already exists
    json_path = obj_name.replace(".md", ".about.json")
    if minio_mgr.object_exists(json_path):
        print(f"⏭️  Skipping (already exists): {json_path}")
        stats = state.get("stats", {})
        stats["skipped"] = stats.get("skipped", 0) + 1

        return {
            **state,
            "current_object": obj_name,
            "markdown": None,  # Skip extraction
            "stats": stats,
        }

    # Download markdown
    md = minio_mgr.download_object(obj_name, as_text=True)

    return {
        **state,
        "current_object": obj_name,
        "markdown": md,
    }


def node_extract_company(state: ScrapeState) -> ScrapeState:
    """
    Node 3: Extract company information using LangExtract.
    """
    md = state.get("markdown")

    if not md:
        # Skipped or failed download
        return {
            **state,
            "company_info": None,
        }

    # Extract company info
    info = extractor.extract_from_markdown_text(md)

    if not info:
        stats = state.get("stats", {})
        stats["errors"] = stats.get("errors", 0) + 1
        return {**state, "company_info": None, "stats": stats}

    return {
        **state,
        "company_info": info,
    }


def node_save_result(state: ScrapeState) -> ScrapeState:
    """
    Node 4: Save extraction result to MinIO as JSON.
    """
    obj_name = state.get("current_object")
    info = state.get("company_info")

    if not obj_name:
        return state

    # If no info extracted or skipped, just increment index
    if not info:
        idx = state.get("index", 0) + 1
        return {
            **state,
            "index": idx,
            "markdown": None,
            "company_info": None,
        }

    # Save JSON
    json_path = obj_name.replace(".md", ".about.json")
    data = info.model_dump()
    success = minio_mgr.upload_json(json_path, data)

    # Update stats
    stats = state.get("stats", {})
    if success:
        stats["success"] = stats.get("success", 0) + 1
    else:
        stats["errors"] = stats.get("errors", 0) + 1

    # Move to next object
    idx = state.get("index", 0) + 1

    return {
        **state,
        "index": idx,
        "markdown": None,
        "company_info": None,
        "stats": stats,
    }


def should_continue(state: ScrapeState) -> str:
    """
    Conditional edge: Continue processing or end.
    """
    objects = state.get("objects", [])
    idx = state.get("index", 0)

    if idx < len(objects):
        return "fetch_markdown"
    return END


def build_graph() -> StateGraph:
    """
    Build and compile the extraction workflow graph.
    """
    graph = StateGraph(ScrapeState)

    # Add nodes
    graph.add_node("list_objects", node_list_objects)
    graph.add_node("fetch_markdown", node_fetch_markdown)
    graph.add_node("extract_company", node_extract_company)
    graph.add_node("save_result", node_save_result)

    # Set entry point
    graph.set_entry_point("list_objects")

    # Add edges
    graph.add_edge("list_objects", "fetch_markdown")
    graph.add_edge("fetch_markdown", "extract_company")
    graph.add_edge("extract_company", "save_result")

    # Add conditional edge for looping
    graph.add_conditional_edges(
        "save_result",
        should_continue,
        {
            "fetch_markdown": "fetch_markdown",
            END: END,
        },
    )

    return graph.compile()


def main():
    """
    Run the extraction workflow.
    """
    print("🚀 Starting LangGraph extraction workflow...")
    print()

    app = build_graph()
    final_state = app.invoke({})

    # Print summary
    stats = final_state.get("stats", {})
    print("\n" + "=" * 60)
    print("📊 Extraction Summary:")
    print(f"  ✅ Successful: {stats.get('success', 0)}")
    print(f"  ⏭️  Skipped: {stats.get('skipped', 0)}")
    print(f"  ❌ Errors: {stats.get('errors', 0)}")
    print(f"  📁 Total: {stats.get('total', 0)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
