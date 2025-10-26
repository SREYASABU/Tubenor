from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.utils.logger import get_controller_logger

from app.database.core import DbSession

from app.agents.main_agent import coordinator_agent
from app.agents.sub_agents.query_to_apicall_agent.agent import query_to_apicall_agent
from app.agents.sub_agents.response_analyzer_agent.agent import response_analyzer_agent
from app.agents.utils import handle_agent_request


logger = get_controller_logger("agents")
router = APIRouter(prefix="/agents", tags=["agents"])

AGENTS = {
    "coordinator": coordinator_agent,
    "query_to_apicall": query_to_apicall_agent,
    "response_analyzer": response_analyzer_agent
}

@router.get("/list", response_model=List[str])
def list_agents() -> List[str]:
    """
    List all available agents in the system.
    """
    return list(AGENTS.keys())

# @router.get("/get/{agent_name}")
# def get_agent(agent_name: str) -> Any:
#     """
#     Retrieve the agent instance based on the agent name.
#     """
#     return AGENTS.get(agent_name)

@router.post("/general-query")
async def handle_general_query(db:DbSession,query: str):
    """
    Handle a general YouTube-related query using the coordinator agent.
    """
    try:
        response = await handle_agent_request(db,query, coordinator_agent)
        return response
    except Exception as e:
        raise


# async def handle_youtube_query(user_query: str) -> Dict[str, Any]:
#     """
#     Handle a YouTube query using the query-to-apicall agent and response analyzer agent.
    
#     Args:
#         user_query: Natural language query about YouTube data
    
#     Returns:
#         Dict containing analyzed results from the YouTube API
#     """
    
#     try:
#         # Step 1: Convert query to API call and execute
#         query = query_utils.build_query(user_query)
#         query = query_utils.pre_process(query)
        
#         api_result = await handle_agent_request(query, query_to_apicall_agent)
#         api_result = query_utils.post_process(api_result)
        
#         try:
#             parsed_api_result = json.loads(api_result)

#         except json.JSONDecodeError as e:
 
#             return {"error": "Failed to parse API response", "raw_response": api_result}
        
#         # Step 2: Analyze the API response
#         analysis_query = analyzer_utils.build_query(parsed_api_result)
#         analysis_query = analyzer_utils.pre_process(analysis_query)
        

#         analysis_result = await handle_agent_request(analysis_query, response_analyzer_agent)
#         analysis_result = analyzer_utils.post_process(analysis_result)
        
#         try:
#             final_result = json.loads(analysis_result)
#             return final_result
#         except json.JSONDecodeError as e:
#             return {"error": "Failed to parse analysis", "raw_response": analysis_result}
            
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Failed to process YouTube query: {str(e)}"
#         )


# async def handle_youtube_analytics_query(
#     metric: str,
#     dimensions: List[str] = None,
#     start_date: str = None,
#     end_date: str = None
# ) -> Dict[str, Any]:
#     """
#     Handle a YouTube Analytics API query with specific metrics and dimensions.
    
#     Args:
#         metric: The analytics metric to retrieve
#         dimensions: Optional list of dimensions to group by
#         start_date: Start date for the analytics data
#         end_date: End date for the analytics data
    
#     Returns:
#         Dict containing analyzed analytics data
#     """
#     try:
#         # Build analytics-specific query
#         analytics_query = {
#             "metric": metric,
#             "dimensions": dimensions or [],
#             "startDate": start_date,
#             "endDate": end_date
#         }
        
#         # Convert to API call
#         query = query_utils.build_analytics_query(analytics_query)
#         query = query_utils.pre_process(query)
        
#         api_result = await handle_agent_request(query, query_to_apicall_agent)
#         api_result = query_utils.post_process(api_result)
        
#         try:
#             parsed_api_result = json.loads(api_result)
#         except json.JSONDecodeError as e:
#             return {"error": "Failed to parse analytics response", "raw_response": api_result}
        
#         # Analyze the analytics data
#         analysis_query = analyzer_utils.build_analytics_query(parsed_api_result)
#         analysis_query = analyzer_utils.pre_process(analysis_query)
        

#         analysis_result = await handle_agent_request(analysis_query, response_analyzer_agent)
#         analysis_result = analyzer_utils.post_process(analysis_result)
        
#         try:
#             final_result = json.loads(analysis_result)
#             return final_result
#         except json.JSONDecodeError as e:
#             return {"error": "Failed to parse analytics analysis", "raw_response": analysis_result}
            
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Failed to process YouTube Analytics query: {str(e)}"
#         )


# async def handle_youtube_search_query(
#     search_query: str,
#     max_results: int = 10,
#     order: str = "relevance",
#     type: str = "video"
# ) -> Dict[str, Any]:
#     """
#     Handle a YouTube Search API query.
    
#     Args:
#         search_query: The search terms
#         max_results: Maximum number of results to return
#         order: Order of results (relevance, date, viewCount, etc.)
#         type: Type of resource to search for (video, channel, playlist)
    
#     Returns:
#         Dict containing analyzed search results
#     """
    
#     try:
#         # Build search-specific query
#         search_params = {
#             "q": search_query,
#             "maxResults": max_results,
#             "order": order,
#             "type": type
#         }
        
#         # Convert to API call
#         query = query_utils.build_search_query(search_params)
#         query = query_utils.pre_process(query)
        
#         # logger.debug("Invoking query-to-apicall agent for search")
#         api_result = await handle_agent_request(query, query_to_apicall_agent)
#         api_result = query_utils.post_process(api_result)
        
#         try:
#             parsed_api_result = json.loads(api_result)
#             # logger.debug("Successfully executed search API call")
#         except json.JSONDecodeError as e:
#             # logger.error(f"Failed to parse search API result as JSON: {str(e)}")
#             return {"error": "Failed to parse search response", "raw_response": api_result}
        
#         # Analyze the search results
#         analysis_query = analyzer_utils.build_search_query(parsed_api_result)
#         analysis_query = analyzer_utils.pre_process(analysis_query)
        
#         # logger.debug("Invoking response analyzer agent for search results")
#         analysis_result = await handle_agent_request(analysis_query, response_analyzer_agent)
#         analysis_result = analyzer_utils.post_process(analysis_result)
        
#         try:
#             final_result = json.loads(analysis_result)
#             # logger.info("Successfully analyzed YouTube Search results")
#             return final_result
#         except json.JSONDecodeError as e:
#             # logger.error(f"Failed to parse search analysis result as JSON: {str(e)}")
#             return {"error": "Failed to parse search analysis", "raw_response": analysis_result}
            
#     except Exception as e:
#         # logger.error(f"Failed to process YouTube Search query: {str(e)}")
#         raise HTTPException(
#             status_code=500,
#             detail=f"Failed to process YouTube Search query: {str(e)}"
#         )
