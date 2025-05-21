# agent-api-main/app/agents/search/tools/profile_search_tool.py
from langchain.tools import tool
from typing import List, Dict, Any, Optional

# Mock database of profiles
mock_profiles_database: List[Dict[str, Any]] = [
    {
        "name": "Alice Wonderland", "title": "Chief Marketing Officer", "company": "Digital Growth Ltd.",
        "location": "San Francisco, CA", "industry": "Software",
        "summary": "Dynamic CMO with 15+ years in B2B SaaS marketing. Expert in demand generation and brand strategy."
    },
    {
        "name": "Bob The Builder", "title": "VP of Engineering", "company": "ConstructTech Solutions",
        "location": "Austin, TX", "industry": "Construction Technology",
        "summary": "Leads high-performing engineering teams to deliver innovative software for the construction industry."
    },
    {
        "name": "Carol Danvers", "title": "Sales Director, EMEA", "company": "Global Fintech Corp",
        "location": "London, UK", "industry": "FinTech",
        "summary": "Results-oriented sales leader expanding market share for a leading FinTech provider in EMEA."
    },
    {
        "name": "David Copperfield", "title": "Product Manager", "company": "RetailMagic Inc.",
        "location": "New York, NY", "industry": "RetailTech",
        "summary": "Product manager focused on e-commerce solutions and customer experience in the retail technology space."
    },
    {
        "name": "Eve Harrington", "title": "Founder & CEO", "company": "GreenSustainables Co.",
        "location": "Portland, OR", "industry": "Sustainability",
        "summary": "Entrepreneur building a company focused on sustainable products and eco-friendly solutions."
    }
]

@tool
def profile_search_tool(
    query: str,
    industry_filter: Optional[List[str]] = None,
    location_filter: Optional[List[str]] = None,
    title_filter: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Searches for profiles based on a general query and optional filters.
    Simulates searching a professional profile database.

    Args:
        query (str): A general search query string (e.g., "B2B SaaS marketing leaders").
        industry_filter (Optional[List[str]]): List of industries to filter by.
        location_filter (Optional[List[str]]): List of locations to filter by.
        title_filter (Optional[List[str]]): List of relevant job titles to filter by.

    Returns:
        List[Dict[str, Any]]: A list of matching profiles (dictionaries).
    """
    print(f"Mock profile_search_tool called with: query='{query}', industries={industry_filter}, locations={location_filter}, titles={title_filter}")
    results: List[Dict[str, Any]] = []

    for profile in mock_profiles_database:
        # In a real tool, 'query' would be used more intelligently.
        # Here, we primarily use filters for the mock.
        
        matches_industry = True
        if industry_filter:
            matches_industry = profile.get("industry", "").lower() in [ind.lower() for ind in industry_filter]

        matches_location = True
        if location_filter:
            profile_loc_lower = profile.get("location", "").lower()
            matches_location = any(loc.lower() in profile_loc_lower for loc in location_filter)

        matches_title = True
        if title_filter:
            profile_title_lower = profile.get("title", "").lower()
            matches_title = any(title.lower() in profile_title_lower for title in title_filter)
        
        # Simple query match (check if any word in query appears in name, title, company, or summary)
        matches_query = True
        if query:
            query_words = query.lower().split()
            profile_text_corpus = f"{profile.get('name','')} {profile.get('title','')} {profile.get('company','')} {profile.get('summary','')}".lower()
            if not any(word in profile_text_corpus for word in query_words):
                matches_query = False


        if matches_query and matches_industry and matches_location and matches_title:
            results.append(profile)

    # Limit results for the mock
    return results[:5]