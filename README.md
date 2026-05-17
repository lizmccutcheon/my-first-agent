# My First Agent
Simple AI agent, built with Python/Gemini-2.5-flash, and a sample application coded with him.

Original agent script was built following the [boot.dev](https://www.boot.dev/) [Build an AI Agent in Python](https://www.boot.dev/courses/build-ai-agent-python) course, but has been extended/cleaned up.

The base bones of the calculator app were also provided as part of this course; various extra features and the REST API were vibe-coded by me with the little bastard. Details in the folder.

## Project Structure

```
.
├── calculator/  # vibe-coded app and FastAPI front-end, see docs in this folder for details on how to run
├── functions/  # functions available to the agent + mechanism to call them.  TODO: cleanup, set up a registry
├── schemas/  # agent types and exceptions.
├── main.py
├── config.py  # global parameters for the agent
├── prompts.py  # starter prompt
└── README.md
```

## Usage
I wouldn't suggest using it, it's a toy agent and pretty unsafe! Here are instructions for running it locally from command line, with a limited blast radius.

1. Install dependencies:
 ```uv sync```
2. Put your Gemini API key in a `.env` file in the root dir: 
```GEMINI_API_KEY=[your secret key]```.   
If you don't have one already, go create one on [Google AI Studio](https://aistudio.google.com/).
3. Update `config.py` with some limits:  
`WORKING_DIR` = the directory the agent is constrained to working inside.  
`MAX_ITERATIONS` = the max number of times agent is allowed to loop without completing. Suggest not allowing it too many or it could get expensive and/or figure out how to break out of jail.  
`MAX_CHARS` = restricts the max number of chars it can read from files (prevents tokens blowing out and becoming expensive).  
4. The default prompt in `prompts.py` can be updated if you like.
5. Get in the root directory and run it with:  
```uv run main.py "Build my brilliant idea which is ..." --verbose --metadata```  
`--verbose` flag is optional: if passed, extra information about function calls, results etc is printed to console at each iteration.  
`--metadata` flag is options: if passed, information about token usage and other response metadata is printed to console at each iteration.  

