from langchain.tools import StructuredTool
from Tools.WeatherApi import weather_by_city
from Tools.TaskApi import run
from Tools.JobSearcherApi import search
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import ToolException
from typing import Optional


def _handle_error(error: ToolException) -> str:
    return (
        "The following errors occurred during tool execution:"
        + error.args[0]
    )

def get_weather_for_today(city: str) -> dict:
    try:
        return weather_by_city(city)
    except Exception:
        raise ToolException("The weather tool is not available.")
    

class WeatherInput(BaseModel):
    city: str = Field(description="city for which weather is looked for")

weather = StructuredTool.from_function(
    func = get_weather_for_today,
    name = "Weather_retriever_for_today",
    description = """useful when you need to answer questions about the weather for TODAY ONLY. 
                     Not for days in the future (eg. 25th, 12th, 5th etc.). 
                     Don't call the tool if there was mentioned any days in the future or in the past 
                     (e.g. tomorrow, the day before, 25th of *any month*)""",
    args_schema = WeatherInput,
    handle_tool_error = _handle_error
)

def create_task(title: str, notes: str=None):
    try:
        return run(title, notes)
    except Exception:
        raise ToolException("The task tool is not available.")
    
class TaskInput(BaseModel):
    title: str = Field(description="The title of a task")
    notes: Optional[str] = Field(None, description="Details which can describe a task")

task_creator = StructuredTool.from_function(
    func = create_task,
    name = "Task_creator",
    description = """useful when user asks to create a task or reminder for him. 
                    E.g. Create a task:'Buy a shampoo' with description:'Two different shampoos for morning and evening'
                    If you didn't understand where is the title, where is the description - ask user for clarification""",
    args_schema=TaskInput,
    handle_tool_error = _handle_error
)

def search_job(position: str, city: str=None):
    try:
        return search(position, city)
    except:
        raise Exception("The search job tool is not available")

class JobInput(BaseModel):
    query: str = Field(description="query for job searching")
    city: Optional[str] = Field(None, description="city in which user is looking for a job")

job_searcher = StructuredTool.from_function(
    func = search_job,
    name = "Job_searcher",
    description="""use it when user looking for job vacancies. 
                E.g. Give me all vacancies: 'software developer' in city: 'London'"""
)