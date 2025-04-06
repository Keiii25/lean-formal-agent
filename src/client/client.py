import json
import requests
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='Math Solver Agent Client')
    parser.add_argument('--host', default='localhost', help='API host')
    parser.add_argument('--port', default='8000', help='API port')
    parser.add_argument('--problem', required=True, help='Math problem to solve using SymPy, e.g., solve(x**2 - 4, x)')
    
    args = parser.parse_args()
    base = f"http://{args.host}:{args.port}"

    try:
        # Step 1: Search for math solver tools
        tools_response = requests.get(f"{base}/tool_search?query=math")
        tools_response.raise_for_status()
        tools = tools_response.json()

        # Step 2: Filter for the Math Solver tool
        math_tool_ids = [
            tool["id"]
            for tool in tools
            if tool["payload"]["id"].lower().startswith("mathsolver")
        ]

        if not math_tool_ids:
            raise Exception("No MathSolver tool found")

        # Step 3: Create agent using MathSolver tool
        agent_response = requests.post(
            f"{base}/save_agent",
            json={
                "name": "Math Solver Agent",
                "description": "Agent for solving math problems using SymPy",
                "arguments": ["query"],
                "agents": {
                    "math_agent": {
                        "role": "Symbolic Math Expert",
                        "goal": "Solve mathematical expressions and equations using SymPy",
                        "backstory": "A math assistant that can solve equations, simplify expressions, and more.",
                        "agent_tools": ["MathSolverTool"],
                    }
                },
                "tasks": {
                    "solve_task": {
                        "description": "{query}",
                        "expected_output": "Solution to the math problem",
                        "agent": "math_agent"
                    }
                }
            }
        )
        agent_response.raise_for_status()
        agent = agent_response.json()

        # Step 4: Call the agent with the user-specified problem
        query = f"Solve this problem: {args.problem}"
        print(args)
        call_response = requests.post(
            url=f"{base}/agent_call",
            params={"agent_id": agent["agent_id"]},
            json={"query": args.problem},
        )
        call_response.raise_for_status()

        # Step 5: Display the result
        print(json.dumps(call_response.json(), indent=2))

    except requests.exceptions.RequestException as e:
        print(f"HTTP Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
