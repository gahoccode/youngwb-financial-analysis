from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

# Import the custom tools for financial analysis
from youngwb.tools.custom_tool import FinancialDataTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Youngwb():
    """Youngwb crew for financial analysis"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # Agent definition from YAML config
        
    @agent
    def financial_analyst(self) -> Agent:
        """Financial analyst agent responsible for analyzing financial statements"""
        # Create financial data tool instance
        financial_tool = FinancialDataTool()
        
        # Create the agent with the tool directly
        return Agent(
            role=self.agents_config['financial_analyst']['role'], # type: ignore[index]
            goal=self.agents_config['financial_analyst']['goal'], # type: ignore[index]
            backstory=self.agents_config['financial_analyst']['backstory'], # type: ignore[index]
            tools=[financial_tool],
            verbose=True
        )

    
    @task
    def financial_analysis_task(self) -> Task:
        """Financial analysis task for analyzing company statements"""
        return Task(
            config=self.tasks_config['financial_analysis_task'], # type: ignore[index]
            output_file='financial_analysis.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Youngwb crew"""
        # For financial analysis, we only need the financial analyst agent and task
        financial_analyst = self.financial_analyst()
        financial_analysis_task = self.financial_analysis_task()
        
        return Crew(
            agents=[financial_analyst],
            tasks=[financial_analysis_task],
            process=Process.sequential,
            verbose=True
        )
