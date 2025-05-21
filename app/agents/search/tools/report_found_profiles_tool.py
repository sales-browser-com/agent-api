# agent-api-main/app/agents/search/tools/report_found_profiles_tool.py
from langchain.tools import tool
from typing import List
from app.models.search import Profile # Using the Pydantic model for type safety

@tool
def report_found_profiles_tool(profiles: List[Profile]) -> str:
    """
    Receives the final list of found profiles that match the ICP.
    This tool confirms that the profiles have been processed and are ready for output.
    The 'profiles' argument MUST be a list of Profile objects.

    Args:
        profiles (List[Profile]): A list of Profile objects, where each Profile object
                                  contains fields like name, title, company, location, industry, summary.

    Returns:
        str: A confirmation message indicating the number of profiles reported.
    """
    # For debugging or logging, you could print the profiles:
    # for p in profiles:
    #     print(f"Reporting profile: {p.model_dump_json(indent=2)}")
    
    if not profiles:
        return "No profiles were reported."
    return f"Successfully reported {len(profiles)} profiles. They are now available."