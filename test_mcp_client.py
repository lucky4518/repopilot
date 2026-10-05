import asyncio

from app.agent.mcp_tools import get_mcp_tools


async def main():

    tools = await get_mcp_tools()

    print()
    print("=" * 70)
    print("MCP TOOLS")
    print("=" * 70)

    for tool in tools:

        print()
        print("Name:")
        print(tool.name)

        print()
        print("Description:")
        print(tool.description)

        print()
        print("-" * 70)


if __name__ == "__main__":
    asyncio.run(main())