import os
import sys
import logging
from dotenv import load_dotenv
import argparse

from google import genai
from google.genai import types
from google.genai import errors

from prompts import system_prompt
from functions.call_function import available_functions, call_function
from schemas.agent import AgentResult
from schemas.exceptions import (
    AgentError,
    AgentIterationLimitError,
    AgentNoCandidatesError,
    MalformedResponseError,
)

from config import MAX_ITERATIONS

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose mode")
parser.add_argument("--metadata", action="store_true", help="Enable metadata mode")

args = parser.parse_args()


load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


client = genai.Client(api_key=API_KEY)


def generate_content(messages: list[types.Content]) -> types.GenerateContentResponse:
    """Send the conversation to Gemini and return the raw response."""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    return response


def log_response_metadata(
    user_prompt: str, response: types.GenerateContentResponse
) -> None:
    """Log response metadata if using metadata mode"""
    if response.usage_metadata is not None:
        usage_metadata = response.usage_metadata
        logger.info(f"User prompt:\n{user_prompt}")
        logger.info(
            f"Prompt tokens: {usage_metadata.prompt_token_count}\nResponse tokens: {usage_metadata.candidates_token_count}"
        )
    else:
        logger.warning("No metadata returned with response.")


def get_function_call_response_content(response, verbose: bool) -> list[types.Part]:
    """Collect function call response parts from a model response."""
    if response.function_calls is None:
        return []

    function_results = []
    for call in response.function_calls:
        function_call_result = call_function(call)

        if not function_call_result.parts:
            raise MalformedResponseError(
                f"call_function returned no parts for {call.name!r}"
            )

        part = function_call_result.parts[0]

        if part.function_response is None:
            raise MalformedResponseError(
                f"part has no function_response for {call.name!r}"
            )

        if part.function_response.response is None:
            raise MalformedResponseError(
                f"function_response has no payload for {call.name!r}"
            )

        function_results.append(part)

        if verbose:
            logger.info(f"-> {part.function_response.response}")

    return function_results


def run_agent(
    user_prompt: str, max_iterations: int, verbose: bool = False, metadata: bool = False
):
    """Run the agent with the specified user prompt. After each reponse, the candidate
    and function call information is added to the model context and repassed with each
    iteration.
    """
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    for i in range(max_iterations):
        response = generate_content(messages=messages)

        if metadata:
            log_response_metadata(user_prompt, response)

        if not response.candidates:
            raise AgentNoCandidatesError("Model returned no candidates, aborting")

        for candidate in response.candidates:
            if candidate.content is None:
                continue
            messages.append(candidate.content)

        function_call_responses = get_function_call_response_content(
            response=response, verbose=verbose
        )
        if not function_call_responses:
            return AgentResult(response_text=response.text, iterations=i + 1)

        messages.append(types.Content(role="user", parts=function_call_responses))

    raise AgentIterationLimitError(MAX_ITERATIONS)


def main():
    try:
        agent_response = run_agent(
            user_prompt=args.user_prompt,
            max_iterations=MAX_ITERATIONS,
            verbose=args.verbose,
            metadata=args.metadata,
        )
        logger.info(f"Final response: {agent_response.response_text}")
        logger.info(
            f"Completed! Final response tool {agent_response.iterations} iterations."
        )
    except AgentError as e:
        logger.error(f"Agent error: {e}", exc_info=True)
        sys.exit(e.exit_code)
    except errors.APIError as e:
        logger.error(f"API error from Gemini: {e}", exc_info=True)
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}", exc_info=True)


if __name__ == "__main__":
    main()
