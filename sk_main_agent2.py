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

# async def check_mcp_dependencies():
#     """Check if MCP dependencies are available"""
#     try:
#         # Check if npx is available
#         result = subprocess.run(['npx', '--version'], capture_output=True, text=True, timeout=10)
#         if result.returncode != 0:
#             return False, "npx is not available. Please install Node.js and npm."
        
#         # Check if @azure/mcp package is accessible
#         result = subprocess.run(['npx', '-y', '@azure/mcp@latest', '--version'], capture_output=True, text=True, timeout=30)
#         if result.returncode != 0:
#             return False, "Failed to access @azure/mcp package. Check your internet connection and npm registry access."
        
#         return True, "MCP dependencies are available"
#     except subprocess.TimeoutExpired:
#         return False, "Timeout checking MCP dependencies"
#     except FileNotFoundError:
#         return False, "npx not found. Please install Node.js and npm."
#     except Exception as e:
#         return False, f"Error checking MCP dependencies: {e}"

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

    # 2. Check MCP dependencies first
    # print("🔍 Checking MCP dependencies...")
    # mcp_available, mcp_message = await check_mcp_dependencies()
    
    # if not mcp_available:
    #     print(f"❌ {mcp_message}")
    #     print("\n📋 To fix this issue:")
    #     print("1. Install Node.js from https://nodejs.org/")
    #     print("2. Restart your terminal/command prompt")
    #     print("3. Run 'npm --version' to verify installation")
    #     print("4. Try running this script again")
        
    #     # Continue without MCP - create a basic agent
    #     print("\n🤖 Creating basic agent without MCP tools...")
    #     agent = ChatCompletionAgent(
    #         service=kernel.get_service("azure_openai"),
    #         name="Azure_Assistant",
    #         instructions="You are an Azure assistant. Since MCP tools are not available, you can provide general Azure guidance and information.",
    #     )
    #     print("✅ Basic Azure Assistant agent created")
        
    #     # Test the basic agent
    #     print("\n🤖 Testing basic agent...")
    #     test_message = "Hello! What can you help me with regarding Azure?"
    #     print(f"📤 Sending message to basic agent: '{test_message}'")
    #     try:
    #         response = await agent.get_response(messages=test_message)
    #         print(f"📥 Basic agent response received: {response}")
    #     except Exception as e:
    #         print(f"❌ Error during basic agent interaction: {e}")
    #         print(f"Error type: {type(e).__name__}")
    #         import traceback
    #         print(f"Full traceback: {traceback.format_exc()}")
        
    #     return

    # 3. Configure and start the Azure MCP server using MCPStdioPlugin
    print("🚀 Starting Azure MCP server...")
    
    now = time.time()
    try:
        async with MCPStdioPlugin(
            name="Azure MCP",
            description="Azure Model Context Protocol server",
            command="npx",
            args=["-y", "@azure/mcp@latest", "server", "start"],
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