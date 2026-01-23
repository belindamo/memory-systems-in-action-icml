"""
ReAct Agent using OpenAI function calling
"""
import json
import openai
from typing import Any, Dict, List, Tuple


class ReActAgent:
    """
    ReAct agent that uses OpenAI function calling to interact with memory tools.
    """
    def __init__(self, adapter, model: str = "gpt-4o", max_iterations: int = 5):
        self.adapter = adapter
        self.model = model
        self.max_iterations = max_iterations
        self.client = openai.OpenAI()

    def run(self, question: str) -> Tuple[str, Dict[str, Any]]:
        """
        Run the agent on a question.

        Returns:
            (answer, trace) where trace contains metrics like tokens, cost, tool_calls
        """
        # Initialize conversation
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant with access to a user's conversation history. "
                    "Use the available tools to search through the conversation history and "
                    "answer the user's question accurately. If you cannot find the answer, "
                    "say 'I don't have enough information to answer that question.'"
                )
            },
            {
                "role": "user",
                "content": question
            }
        ]

        # Get available tools from adapter
        tools = self.adapter.get_tools()

        # Tracking
        total_tokens = 0
        total_cost = 0.0
        tool_calls_count = 0
        iterations = 0

        # ReAct loop
        for iteration in range(self.max_iterations):
            iterations = iteration + 1

            # Call LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None
            )

            # Track usage
            usage = response.usage
            total_tokens += usage.total_tokens
            total_cost += self._calculate_cost(usage, self.model)

            message = response.choices[0].message
            messages.append(message.model_dump(exclude_unset=True))

            # Check if done (no tool calls)
            if not message.tool_calls:
                answer = message.content
                break

            # Execute tool calls
            tool_calls_count += len(message.tool_calls)
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Call adapter
                result = self.adapter.execute_tool(function_name, function_args)

                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })
        else:
            # Max iterations reached
            answer = "I ran out of time to answer this question."

        trace = {
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "tool_calls": tool_calls_count,
            "iterations": iterations
        }

        return answer, trace

    def _calculate_cost(self, usage, model: str) -> float:
        """Calculate cost based on OpenAI pricing (as of Jan 2025)"""
        # GPT-4o pricing (per 1M tokens)
        if model == "gpt-4o":
            input_cost_per_1m = 2.50
            output_cost_per_1m = 10.00
        elif model == "gpt-4o-mini":
            input_cost_per_1m = 0.15
            output_cost_per_1m = 0.60
        else:
            # Default to gpt-4o pricing
            input_cost_per_1m = 2.50
            output_cost_per_1m = 10.00

        input_cost = (usage.prompt_tokens / 1_000_000) * input_cost_per_1m
        output_cost = (usage.completion_tokens / 1_000_000) * output_cost_per_1m

        return input_cost + output_cost
