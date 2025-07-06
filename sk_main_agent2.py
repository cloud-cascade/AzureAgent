import asyncio
import time
import os
import subprocess
import sys
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
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY")
        )
    )
    print("✅ Azure OpenAI service configured")

    # 2. Configure and start the Azure MCP server using the working pattern
    print("🚀 Starting Azure MCP server...")
    
    # Define parameters matching the working OpenAI framework
    params = {"command": "npx", "args": ["-y", "@azure/mcp@latest", "server", "start"]}
    
    # Optional: Apply a tool filter if needed
    # def rg_only(tool):
    #     # Implement your filtering logic here
    #     return "resource_group" in tool.name.lower()
    # tool_filter = rg_only

    now = time.time()
    try:
        async with MCPStdioPlugin(
            name="Azure MCP",
            description="Azure Model Context Protocol server",
            command=params["command"],
            args=params["args"],
            # tool_filter=tool_filter, # Uncomment and configure if filtering is needed
        ) as mcp_plugin:
            print(f"✅ Azure MCP server started in {time.time() - now:.2f} seconds")

            # 3. Add the MCP plugin to the kernel
            kernel.add_plugins([mcp_plugin])
            print("✅ MCP plugin added to kernel")

            # 4. Create and use the agent
            agent = ChatCompletionAgent(
                service=kernel.get_service("azure_openai"),
                name="Azure_Assistant",
                instructions="You can interact with Azure services through the available tools. Be helpful and provide clear information about Azure resources.",
            )
            print("✅ Azure Assistant agent created")

            # Example interaction
            print("\n🤖 Testing agent...")
            test_message = "List all the storage accounts?"
            print(f"📤 Sending message to agent: '{test_message}'")
            try:
                response = await agent.get_response(messages=test_message)
                print(f"📥 Agent response received: {response}")
            except Exception as e:
                print(f"❌ Error during agent interaction: {e}")
                print(f"Error type: {type(e).__name__}")
                import traceback
                print(f"Full traceback: {traceback.format_exc()}")

    except Exception as e:
        print(f"❌ Failed to start Azure MCP server: {e}")
        print("\nTroubleshooting tips:")
        print("1. Ensure you're authenticated with Azure (az login)")
        print("2. Check your Azure subscription and permissions")
        print("3. Verify the @azure/mcp package exists and is accessible")
        print("4. Try running the MCP server manually first")
        print("5. Check if you have proper internet connectivity")

if __name__ == "__main__":
    asyncio.run(main())