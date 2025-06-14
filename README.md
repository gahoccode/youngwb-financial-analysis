# YoungWB Financial Analysis

Welcome to the YoungWB Financial Analysis project, a specialized financial analysis tool powered by [crewAI](https://crewai.com). This project uses AI agent orchestration to perform comprehensive analysis of Vietnamese stock market financial statements, providing insights on profitability, liquidity, solvency, cash flow, and dividend sustainability.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/youngwb/config/agents.yaml` to define your agents
- Modify `src/youngwb/config/tasks.yaml` to define your tasks
- Modify `src/youngwb/crew.py` to add your own logic, tools and specific args
- Modify `src/youngwb/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the YoungWB Crew, assembling the agents and assigning them tasks as defined in your configuration.

## Financial Analysis Features

- **Comprehensive Financial Analysis**: Analyzes balance sheets, income statements, and cash flow statements
- **Vietnamese Stock Market Support**: Integrates with vnstock for data retrieval of Vietnamese equities
- **Multiple Analysis Types**: Profitability, liquidity, solvency, cash flow, and dividend analysis
- **Agent-based Architecture**: Financial analyst agent performs specialized financial analysis using CrewAI

## Usage Examples

```bash
# Run analysis on a specific ticker (e.g., REE)
crewai run
```

## Project Structure

The project follows a modular architecture:
- `config/`: YAML configuration files for agents and tasks
- `tools/`: Custom CrewAI tools for financial analysis
- `crew.py`: CrewAI setup and orchestration
- `main.py`: Entry point with CLI support

## Environment Variables

This project requires the following environment variables to be set in a `.env` file in the root directory:

```bash
# OpenAI model to use (e.g., gpt-4o-mini, gpt-4-turbo)
MODEL=gpt-4o-mini

# Your OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here

# Serper API key for web search capabilities
# Get your free Serper API key from https://serper.dev
SERPER_API_KEY=your_serper_api_key_here
```

### API Key Requirements

- **OPENAI_API_KEY**: Required for all agents to function
- **SERPER_API_KEY**: Required for the news research agent to search for Vietnamese stock market news

Without these API keys, certain functionality will be limited or unavailable.
