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
from semantic_kernel.contents import ChatHistory
import logging
import appinsights_opentelemetry
from typing import Optional

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

class AzureAgentService:
    def __init__(self):
        self.kernel = None
        self.agent = None
        self.mcp_plugin = None
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize the Azure agent with MCP server"""
        if self.is_initialized:
            return
            
        try:
            # 1. Initialize Semantic Kernel with Azure OpenAI
            self.kernel = Kernel()
            
            # Get environment variables with validation
            deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
            endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            
            if not all([deployment_name, endpoint, api_key]):
                raise ValueError("Missing required Azure OpenAI environment variables")
            
            self.kernel.add_service(
                AzureChatCompletion(
                    service_id="azure_openai",
                    deployment_name=deployment_name,
                    endpoint=endpoint,
                    api_key=api_key
                )
            )

            # 2. Configure and start the Azure MCP server
            params = {"command": "npx", "args": ["-y", "@azure/mcp@latest", "server", "start"]}
            
            self.mcp_plugin = MCPStdioPlugin(
                name="Azure MCP",
                description="Azure Model Context Protocol server",
                command=params["command"],
                args=params["args"]
            )
            
            await self.mcp_plugin.__aenter__()
            
            # 3. Add the MCP plugin to the kernel
            self.kernel.add_plugin(self.mcp_plugin, plugin_name="AzureMCP")
            
            # 4. Create the agent with MCP tools
            self.agent = ChatCompletionAgent(
                service=self.kernel.get_service("azure_openai"),
                kernel=self.kernel,
                name="Azure_Assistant",
                instructions="You can interact with Azure services through the available tools. Be helpful and provide clear information about Azure resources. You can also use the tools to get information about Azure resources. You can also use the tools to create and manage Azure resources. You can also use the tools to delete and manage Azure resources.",
            )
            
            self.is_initialized = True
            
        except Exception as e:
            raise Exception(f"Failed to initialize Azure agent: {e}")
    
    async def get_response(self, message: str) -> str:
        """Get response from the Azure agent"""
        if not self.is_initialized:
            await self.initialize()
        
        try:
            response = await self.agent.get_response(messages=message)
            return str(response)
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.mcp_plugin:
            await self.mcp_plugin.__aexit__(None, None, None)

# Global agent service instance
agent_service = AzureAgentService()

def run_async_function(func, *args, **kwargs):
    """Helper function to run async functions"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(func(*args, **kwargs))
    finally:
        loop.close()

def initialize_agent():
    """Initialize the agent service"""
    return run_async_function(agent_service.initialize)

def get_agent_response(message: str) -> str:
    """Get response from the agent service"""
    return run_async_function(agent_service.get_response, message)

def cleanup_agent():
    """Cleanup the agent service"""
    return run_async_function(agent_service.cleanup)

def is_agent_initialized() -> bool:
    """Check if agent is initialized"""
    return agent_service.is_initialized 