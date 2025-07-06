import asyncio
import time
import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.mcp import MCPStdioPlugin
from semantic_kernel.agents import ChatCompletionAgent

# Load environment variables from .env file
load_dotenv()

async def main():
    # 1. Initialize Semantic Kernel with Azure OpenAI
    kernel = Kernel()
    kernel.add_service(
        AzureChatCompletion(
            service_id="azure_openai",
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),  # Replace with your deployment name
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),  # Replace with your endpoint
            api_key=os.getenv("AZURE_OPENAI_API_KEY")  # Replace with your API key
        )
    )

    # 2. Configure and start the Azure MCP server using MCPStdioPlugin
    params = {"command": "npx", "args": ["-y", "@azure/mcp@latest", "server", "start"]}
    
    # Optional: Apply a tool filter if needed
    # def rg_only(tool):
    #     # Implement your filtering logic here
    #     return "resource_group" in tool.name.lower()
    # tool_filter = rg_only

    now = time.time()
    async with MCPStdioPlugin(
        name="Azure MCP",  # A name for the plugin in SK
        description="Azure Model Context Protocol server", # Description
        command=params["command"],
        args=params["args"],
        # tool_filter=tool_filter, # Uncomment and configure if filtering is needed
    ) as mcp_plugin:
        print(f"Azure MCP server started in {time.time() - now} seconds")

        # 3. Add the MCP plugin to the kernel
        kernel.add_plugins([mcp_plugin])

        # 4. Use the Azure tools in your agent
        # (Assuming you have defined an agent, e.g., using ChatCompletionAgent)
        agent = ChatCompletionAgent(
            service=kernel.get_service("azure_openai"),
            name="Azure Assistant",
            instructions="You can interact with Azure services through the available tools.",
        )

        # Example prompt:
        response = await agent.get_response(messages="List my Azure Storage containers")
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
