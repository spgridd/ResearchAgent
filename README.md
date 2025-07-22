
-----

# Advanced Autonomous Research Agent

This project showcases an advanced autonomous research agent built with the Google Agent Development Kit (ADK) and deployed on Vertex AI. The agent is designed to autonomously plan, execute, critique, and refine its own research process to answer complex user queries. It features a multi-agent architecture that mimics a human research workflow, exposed through an interactive Streamlit web application.

-----

## Table of Contents

  * [Key Features](https://www.google.com/search?q=%23-key-features)
  * [System Architecture](https://www.google.com/search?q=%23%EF%B8%8F-system-architecture)
  * [Tools & Capabilities](https://www.google.com/search?q=%23%EF%B8%8F-tools--capabilities)
  * [Getting Started](https://www.google.com/search?q=%23%EF%B8%8F-getting-started)
  * [How to Use](https://www.google.com/search?q=%23-how-to-use)

-----

## Key Features

  * **Autonomous Planning**: The agent can break down a complex research question into a step-by-step plan.
  * **Multi-Tool Execution**: It can use various tools to gather information, including web search, financial data search, and internal document search.
  * **Iterative Refinement**: The system employs a critique-and-refine loop, allowing it to improve its answers over multiple iterations for higher quality results.
  * **Dynamic Report Generation**: The agent can synthesize its findings into a coherent report, with an option to generate more detailed and comprehensive outputs.
  * **Interactive Web Interface**: A user-friendly chat interface built with Streamlit allows for easy interaction with the agent.

-----

## System Architecture

The core of this project is a multi-agent system where each agent has a specialized role. These agents work together within a loop to produce the final research report. The `LoopAgent` orchestrates this process for a maximum of 3 iterations, ensuring the output is progressively refined.

The workflow is as follows:
`Planner` → `Executor` → `Synthesizer` → `Critique` → (Loop or Exit)

1.  **PlannerAgent**: This agent receives the user's research query and creates a detailed, step-by-step plan to address it. It determines what information needs to be found and in what order.
2.  **ExecutorAgent**: Following the plan from the Planner, this agent executes each step. It uses a suite of tools to gather the necessary data from different sources.
3.  **SynthesizerAgent**: Once the data is collected, this agent takes the raw information and formats it into a well-structured, human-readable answer. The final response shown to the user comes from this agent.
4.  **CritiqueAgent**: This agent reviews the synthesized report for quality, accuracy, and completeness. Using its `exit_loop` tool, it decides if the answer is satisfactory or if another refinement loop is needed to improve it.

-----

## Tools & Capabilities

The agent's `ExecutorAgent` is equipped with a variety of tools to perform its research tasks:

  * `document_search`: Searches an internal repository of documents for relevant information.
  * `web_search_tool`: Conducts web searches to find up-to-date public information.
  * `finance_tool`: Retrieves specific financial data.
  * `canvas_tool`: Used by the `SynthesizerAgent` to format and present the final answer.

-----

## Getting Started

Follow these steps to set up and run the project locally.

### 1\. Prerequisites

  * Python 3.10+
  * A Google Cloud project with the Vertex AI API enabled.
  * The Google Cloud CLI installed and configured on your local machine.

### 2\. Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/spgridd/ResearchAgent.git
    cd ResearchAgent
    ```

2.  **Authenticate with Google Cloud:**
    Log in with your Google Cloud account. This command will store your credentials locally, allowing the application to use Vertex AI services.

    ```bash
    gcloud auth application-default login
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables (for Langfuse):**
    Create a `.env` file in the root directory. This is used for observability with Langfuse.

    ```
    # .env
    LANGFUSE_SECRET_KEY="your-langfuse-secret-key"
    LANGFUSE_PUBLIC_KEY="your-langfuse-public-key"
    ```

### 3\. Running the Application

Launch the Streamlit web interface with the following command:

```bash
streamlit run app.py
```

-----

## How to Use

1.  Open your browser and navigate to the local Streamlit URL.
2.  Use the chat input box to ask your research question.
3.  For more in-depth answers, enable the **"Create Longer Reports"** toggle at the top of the page.
4.  The agent will process your request, and the final, synthesized answer will appear on the screen. Your chat history will be maintained during the session.