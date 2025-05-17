from langchain.tools import tool
from app.agents.icp.tools.structured_output import ICPData


@tool
def icp_output_tool(input_data: ICPData) -> ICPData:
    """
    Process and return the Ideal Customer Profile (ICP) data.

    This tool receives structured ICP data containing targeting parameters for
    potential customers and returns the processed data. It helps formalize the
    ideal customer profile for targeted outreach.

    Args:
        input_data (ICPData): The structured ICP data containing targeting parameters
                             such as industries, locations, job titles, etc.

    Returns:
        ICPData: The processed ICP data object.
    """
    return input_data