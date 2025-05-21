# agent-api-main/app/agents/search/tools/profile_search_tool.py
from langchain.tools import tool
from typing import List, Dict, Any, Optional
from duckduckgo_search import DDGS # Changed import

@tool
def profile_search_tool(
    query: str,
    industry_filter: Optional[List[str]] = None,
    location_filter: Optional[List[str]] = None,
    title_filter: Optional[List[str]] = None,
    max_results: int = 7 # Keep low to avoid too much data for LLM & rate limits
) -> List[Dict[str, Any]]:
    """
    Searches the internet using DuckDuckGo for profiles or information matching the query and filters.
    It's best to use specific keywords in the query, like job titles, company names, or skills,
    combined with locations or industries. For example, 'LinkedIn profile John Doe Marketing Manager SaaS San Francisco'.

    Args:
        query (str): The primary search query string. Should be specific.
                     Incorporate keywords related to the ICP here.
        industry_filter (Optional[List[str]]): List of industries. These will be appended to the query.
        location_filter (Optional[List[str]]): List of locations. These will be appended to the query.
        title_filter (Optional[List[str]]): List of job titles. These will be appended to the query.
        max_results (int): Maximum number of search results to return. Defaults to 7.

    Returns:
        List[Dict[str, Any]]: A list of search results, where each result is a dictionary
                              containing 'title', 'href' (URL), and 'body' (snippet).
                              Returns an error message list if search fails.
    """
    
    full_query = query
    
    # Construct a more targeted query
    filter_parts = []
    if title_filter:
        # For titles, often helps to have them explicitly in the query
        # Using "OR" for multiple titles might be too broad for DDG, 
        # LLM should try one specific title at a time or a concise primary title.
        # Or LLM can make multiple calls if needed.
        # We'll let the LLM formulate the main query string carefully.
        # The filters here will be simple appends.
        filter_parts.extend(f'"{t}"' for t in title_filter)
    if industry_filter:
        filter_parts.extend(industry_filter)
    if location_filter:
        filter_parts.extend(location_filter)

    if filter_parts:
         full_query += " " + " ".join(filter_parts)

    # Ensure query is not overly long for DDG
    # A more sophisticated approach might be needed if queries become too complex
    full_query = (full_query[:450] + '...') if len(full_query) > 450 else full_query

    print(f"Executing internet search with DDGS using query: '{full_query}', max_results={max_results}")

    results = []
    try:
        # DDGS is a context manager
        with DDGS() as ddgs:
            search_results = ddgs.text(
                keywords=full_query,
                region='wt-wt', # World-wide
                safesearch='moderate', # Moderate, off, strict
                timelimit=None, # Past day, week, month, year
                max_results=max_results
            )
            if search_results:
                for r in search_results: # search_results is a generator
                    results.append({
                        "title": r.get("title"),
                        "href": r.get("href"),
                        "body": r.get("body") # Snippet
                    })
    except Exception as e:
        error_message = f"Error during DuckDuckGo search: {str(e)}. Query: '{full_query}'"
        print(error_message)
        return [{"error": error_message, "query_attempted": full_query}]

    if not results:
        return [{"message": f"No results found for the query: '{full_query}'"}]
        
    return results