class AgentError(Exception):
    """Base class for Agent exceptions"""
    exit_code = 1


class AgentIterationLimitError(AgentError):
    """Raised when the interation budget is exceeded."""
    def __init__(self, max_iterations: int):
        self.max_iterations = max_iterations
        super().__init__(
            f"Agent did not complete within {max_iterations}"
        )

         
class AgentNoCandidatesError(AgentError):
    """Raised when no candidates are returned. Can indicate API safety blocking."""


class MalformedResponseError(AgentError): 
    """Raised when expected component of API reponse are missing"""