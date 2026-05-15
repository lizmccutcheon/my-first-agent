from dataclasses import dataclass

@dataclass
class AgentResult:
    response_text: str
    iterations: int
    # add tokens_used, function_calls_made, etc.