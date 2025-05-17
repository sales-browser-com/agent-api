from langchain.tools import tool

from app.models.icp import ICPData


@tool
def icp_output_tool(input_data: ICPData) -> str:
    """
    Receives the Ideal Customer Profile (ICP) data formulated by the LLM.

    This tool acts as a confirmation step. The LLM prepares the ICPData
    and passes it to this tool. The tool itself currently just returns a
    success message. Future enhancements could involve storing or validating
    the ICPData.

    Args:
        input_data (ICPData): The structured ICP data containing targeting parameters
                             such as industries, locations, job titles, etc.,
                             as populated by the LLM.

    Returns:
        str: A confirmation message indicating the ICP data was received.
    """
    # In a real scenario, you might save input_data to a database here
    # print(f"ICP Data received by tool: {input_data.model_dump_json(indent=2)}")
    return "Icp is updated successfully"
