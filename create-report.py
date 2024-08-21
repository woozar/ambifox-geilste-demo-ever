from langchain.tools import tool
from typing import List
from datetime import datetime
from enum import Enum
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_tools_agent, AgentExecutor
from typing import TypedDict


class Site(TypedDict):
    """A site refers to a specific location or facility where a company conducts its operations. This site could be an office, a manufacturing plant, a retail store, a warehouse, or any other type of physical space owned or leased by the business."""

    id: str
    name: str
    description: str


class Device(TypedDict):
    """A device is a piece of hardware or software that is doing something and connected to the network."""

    id: str
    name: str
    description: str


class Metric(TypedDict):
    """A metric is a value that is measured on a device."""

    id: str
    name: str
    description: str
    unit: str


@tool
def getSites() -> List[Site]:
    """Loads and returns a list of all sites of the company"""
    # Implementation of getSites goes here

    return [
        {
            "id": "abc123",
            "name": "Ahaus",
            "description": "Manufacturing facility in Ahaus",
        }
    ]


@tool
def getDevices(siteId: str) -> List[Device]:
    """Loads and returns a list of device that are located at the site"""
    # Implementation of loadSites goes here
    return []  # Placeholder return


@tool
def getMetrics(deviceId: str) -> List[Metric]:
    """Loads and returns a list of metrics that are measured on the device"""
    # Implementation of loadSites goes here
    return []  # Placeholder return


class Aggregation(Enum):
    """Enum representing different types of data aggregation methods."""

    SUM = "sum"
    AVERAGE = "average"
    MIN = "min"
    MAX = "max"
    COUNT = "count"


@tool
def getValues(
    metricId: str,
    deviceId: str,
    start: datetime,
    end: datetime,
    interval: int,
    aggregation: Aggregation,
) -> List[float]:
    """Loads and returns a list of values that are measured on the metric"""
    # Implementation of loadSites goes here
    return []  # Placeholder return


toolkit = [getSites, getDevices, getMetrics, getValues]

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-2024-08-06", temperature=0)

systemPrompt = """
You are an intelligent assistant tasked with creating detailed reports based on user requests. Your goal is to retrieve relevant data from a set of tools and return the results in a well-structured report, formatted using Markdown. The report may include textual descriptions, tables, and mermaid diagrams where appropriate.

Available Tools:

Site Listing Tool

Function: Retrieve and list all available sites.
Usage Example: "List all available sites."
Device Listing Tool

Function: Retrieve and list all devices under a specific site.
Usage Example: "List all devices at Site A."
Metric Listing Tool

Function: Retrieve and list all available metrics for a specific device.
Usage Example: "List all metrics for Device X."
Metric Value Retrieval Tool

Function: Obtain the values of a specific metric for a given device within a specified timeframe and aggregation method.
Parameters:
Device ID or Name
Metric Name
Start Time
End Time
Aggregation Method (e.g., average, sum, max, min)
Usage Example: "Get the average temperature for Device X from 2024-08-01 to 2024-08-07."
Expected Output Format:

Textual Description: Provide concise and informative summaries where applicable.

Tables: Organize numerical data and lists in clear, readable tables.

Mermaid Diagrams: Visualize data relationships or trends using mermaid syntax for diagrams like flowcharts, pie charts, or line graphs.

Example Request:

"Create a report for Site A that includes a list of all devices, the metrics available for Device X, and the average temperature of Device X from 2024-08-01 to 2024-08-07."

Example Response:

# Report for Site A

## Device List
- Device 1: Temperature Sensor
- Device 2: Humidity Sensor

## Metrics for Device X
- Temperature
- Humidity

## Average Temperature for Device X (2024-08-01 to 2024-08-07)
| Date       | Average Temperature (°C) |
|------------|---------------------------|
| 2024-08-01 | 22.5                       |
| 2024-08-02 | 23.0                       |
| 2024-08-03 | 21.8                       |
| 2024-08-04 | 22.1                       |
| 2024-08-05 | 22.4                       |
| 2024-08-06 | 23.2                       |
| 2024-08-07 | 21.9                       |

## Temperature Trend for Device X
```mermaid
graph LR
    A[2024-08-01] -->|22.5°C| B[2024-08-02]
    B -->|23.0°C| C[2024-08-03]
    C -->|21.8°C| D[2024-08-04]
    D -->|22.1°C| E[2024-08-05]
    E -->|22.4°C| F[2024-08-06]
    F -->|23.2°C| G[2024-08-07]
vbnet
Code kopieren

**Guidelines:**

- **Accuracy:** Ensure data is accurately retrieved and presented according to the user request.
- **Clarity:** Structure the report to be easily understood, with clear headings and formatted sections.
- **Completeness:** Ensure that all requested information is included in the final report.
- **Diagrams:** Use mermaid diagrams where it aids in understanding the data or trends.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            systemPrompt,
        ),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)


agent = create_openai_tools_agent(llm, toolkit, prompt)
agent_executor = AgentExecutor(agent=agent, tools=toolkit, verbose=True)

result = agent_executor.invoke(
    {
        "input": "what is the temperature of my router in Ahaus for the last 24 hours. Please draw a line chart."
    }
)
