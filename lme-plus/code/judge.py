"""
LLM Judge for evaluating answer correctness
"""
import openai


class LLMJudge:
    """
    Uses GPT-4o as a judge to evaluate if agent answer matches gold answer.
    Follows LongMemEval evaluation protocol.
    """
    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.client = openai.OpenAI()

    def evaluate(self, question: str, agent_answer: str, gold_answer: str) -> bool:
        """
        Evaluate if agent_answer is semantically equivalent to gold_answer.

        Returns:
            True if correct, False otherwise
        """
        prompt = f"""You are evaluating the correctness of an answer to a question.

Question: {question}

Reference Answer: {gold_answer}

Agent Answer: {agent_answer}

Determine if the Agent Answer is semantically equivalent to the Reference Answer.
- The answers don't need to match word-for-word
- They should convey the same core information
- Minor differences in phrasing or detail are acceptable
- If the agent says it doesn't know or can't answer, that's incorrect (unless the reference is about abstention)

Respond with ONLY one word: "CORRECT" or "INCORRECT"
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=10
        )

        judgment = response.choices[0].message.content.strip().upper()

        return judgment == "CORRECT"
