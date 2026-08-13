# 1. GET THE TOOLS NEEDED TO TALK TO AZURE AI
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# 2. WHERE IS MY AI SERVICE?
endpoint = "MY_ENDPOINT"

# 3. WHICH DEPLOYMENT DO I WANT TO USE?
deployment_name = "model-router"

# 4. PROVE TO AZURE THAT I AM AUTHORISED
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "MY_AZURE_SCOPE"
)

# 5. CREATE THE CLIENT THAT TALKS TO THE SERVICE
client = OpenAI(
    base_url=endpoint,
    api_key=token_provider
)

# 6. SEND A USER MESSAGE TO THE MODEL
completion = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ],
)

# 7. GET THE MODEL'S RESPONSE AND DISPLAY IT
print(completion.choices[0].message)

#--------------Agenttrace- meta-data---------------
"""
One important distinction

What you did with Web Search demonstrates the same retrieve → ground/contextualize → generate pattern, but when Microsoft talks specifically about RAG with enterprise knowledge, you'll often see something like:

Question
   ↓
Search your knowledge base
   ↓
Retrieve relevant chunks/documents
   ↓
Give those chunks to the model
   ↓
Generate grounded answer
---------------------------------------------
Model = the intelligence generating/reasoning about the answer.
Instructions = tell the agent how it should behave.
Tools = capabilities it can invoke when needed.
Web Search = one tool giving access to current external information.
Knowledge = can ground an agent in connected information such as company documents.
Trace = lets the developer see what happened during an execution.

--------------------------------------------------------

The overall journey was:

MY QUESTION
    ↓
AGENT
    ↓
WEB SEARCH TOOL
    ↓
MODEL USES RETRIEVED INFORMATION
    ↓
ANSWER
    ↓
TRACE RECORDS WHAT HAPPENED


-----------------------------------------
1. IDENTITY — WHICH OPERATION IS THIS?
-----------------------------------------

"name":
    A unique name/ID for this particular response operation.

I do NOT need to memorise the ID.


-----------------------------------------
2. CONTEXT — WHICH TRACE DOES IT BELONG TO?
-----------------------------------------

"context": {
    "trace_id": "...",
    "span_id": "...",
    "conversation_id": "..."
}

trace_id:
    Identifies the overall trace/journey.

conversation_id:
    Identifies the conversation this operation belongs to.

span_id:
    Identifies this particular operation within the trace.

Think:

CONVERSATION / TRACE
        ↓
individual operations (spans)
        ↓
web search, response, etc.


-----------------------------------------
3. WHAT KIND OF OPERATION WAS THIS?
-----------------------------------------

"kind": "Response"

This particular trace item represents the RESPONSE operation.


-----------------------------------------
4. PARENT — WHAT DID THIS BELONG TO?
-----------------------------------------

"parent_id": "..."

Connects this operation to its parent in the trace.

This is how Foundry can build the tree I saw:

Conversation
    ↓
Response
    ├── web_search
    └── message


-----------------------------------------
5. STATUS — DID IT WORK?
-----------------------------------------

"status": {
    "status_code": "OK"
}

OK = this operation completed successfully.


-----------------------------------------
6. INPUT — WHAT DID I ASK?
-----------------------------------------

"inputs": {
    "type": "userInput",
    "messages": [
        "What is the current weather in London right now?..."
    ]
}

This records the USER INPUT sent into the agent.


-----------------------------------------
7. OUTPUT — WHAT DID THE AGENT RETURN?
-----------------------------------------

"output": {
    "type": "agentOutput",
    "messages": [
        "Here's the current weather..."
    ]
}

This records the AGENT OUTPUT returned to me.

Important distinction:

INPUT  = what went in
OUTPUT = what came back


-----------------------------------------
8. DURATION — HOW LONG DID IT TAKE?
-----------------------------------------

"duration": 5

The request took about 5 seconds.

This is useful when monitoring performance.


-----------------------------------------
9. TOKEN USAGE — HOW MUCH MODEL PROCESSING?
-----------------------------------------

"usage_info": {
    "prompt_tokens": 11185,
    "completion_tokens": 274,
    "total_tokens": 11459
}

prompt_tokens:
    Tokens processed as INPUT to the model.

completion_tokens:
    Tokens generated as OUTPUT.

total_tokens:
    Input + output tokens.

11185 + 274 = 11459

Important:
My visible question was tiny.
The prompt-token count can include much more context involved
in the agent/tool operation than just the words I typed.

Tokens matter because they relate to model usage and potentially cost.


-----------------------------------------
10. TIMES — WHEN DID THE OPERATION HAPPEN?
-----------------------------------------

"start_time": "..."
"end_time": "..."

Records when processing started and ended.

Useful for monitoring and troubleshooting.


=========================================
WHAT I NEED TO REMEMBER FOR AI-901
=========================================

A TRACE lets me inspect what happened during an agent operation.

It can help show:

- what input was received
- what operations/tools were used
- what output was produced
- whether operations succeeded
- how long they took
- token usage

I do NOT need to memorise trace IDs or JSON syntax.

The important concept is:

QUESTION
   ↓
AGENT
   ↓
TOOL CALL(S)
   ↓
MODEL / PROCESSING
   ↓
RESPONSE

TRACE = visibility into that journey.
"""
#-----------------------diagram----------------------------
"""
                 AGENT
                   │
        ┌──────────┼───────────┐
        ↓          ↓           ↓
 Instructions    Model       Tools
 "behave        router      Web Search
  like this"
                   │
                   ↓
              Guardrails
             "boundaries"
                   
Knowledge → company/connected information
Trace     → observe what happened



"""
#---------------diagram2--------------

"""
AGENT
│
├── MODEL
│   └── model-router
│
├── INSTRUCTIONS
│   └── how it should behave
│
├── TOOLS
│   └── Web Search → something it can DO
│
├── KNOWLEDGE
│   └── information it can retrieve/ground answers in
│
└── GUARDRAILS
    └── safety/security boundaries
"""

#--------------------Evaluation-----
"""
GUARDRAIL
tries to CONTROL unsafe/unwanted behaviour

EVALUATION
MEASURES how well/safely the system performs

TRACE
shows you WHAT HAPPENED during an individual run

"""
#-----------evaluation sequence-------------
"""
Evaluation data
      ↓
test inputs/questions
      ↓
Agent produces responses
      ↓
Evaluators judge those responses
      ↓
Metrics / scores
"""

#------AI-901 architecture picture----------------

"""
                         ┌─────────────────────┐
                         │        USER         │
                         │ asks a question     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────┐
                    │          AGENT              │
                    │                             │
                    │ Instructions / behaviour    │
                    │ "You are an AI-901 study   │
                    │ assistant..."               │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │       MODEL / ROUTER        │
                    │                             │
                    │ Language understanding      │
                    │ Reasoning                   │
                    │ Response generation         │
                    └──────────────┬──────────────┘
                                   │
                     ┌─────────────┴──────────────┐
                     │                            │
                     ▼                            ▼
          ┌────────────────────┐       ┌────────────────────┐
          │       TOOLS        │       │     KNOWLEDGE      │
          │                    │       │                    │
          │ Web search         │       │ Company documents  │
          │ APIs/actions etc.  │       │ Enterprise data    │
          └─────────┬──────────┘       └─────────┬──────────┘
                    │                            │
                    ▼                            ▼
          Live external data              RAG / grounding
                    │                            │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │      RESPONSE       │
                       │                     │
                       │ Grounded answer     │
                       │ + sources where     │
                       │ appropriate         │
                       └──────────┬──────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
          ┌──────────────────┐        ┌──────────────────┐
          │      TRACES      │        │   EVALUATIONS    │
          │                  │        │                  │
          │ What happened?   │        │ How good was it? │
          │ Tool calls       │        │ Test datasets    │
          │ Tokens           │        │ Ground truth     │
          │ Duration         │        │ Benchmarks       │
          └──────────────────┘        └──────────────────┘

                    ┌─────────────────────────┐
                    │       GUARDRAILS        │
                    │                         │
                    │ Safety / security       │
                    │ Content controls        │
                    │ Jailbreak protection    │
                    └─────────────────────────┘
"""

#––––––––––––––––––––––Definitions–––––––––––––––––––––––––––
"""
The biggest distinction: model vs agent

This is one I particularly want you to remember.

A model is the underlying AI capability.

An agent builds behaviour around that capability.

Think of it like:

MODEL
"The brain"

       +

INSTRUCTIONS
"What role should you perform?"

       +

TOOLS
"What can you do?"

       +

KNOWLEDGE
"What additional information can you access?"

       +

GUARDRAILS
"What boundaries must you follow?"

       =

AGENT

So if an exam scenario says:

"The system needs to reason over a user's request "
"and decide when to use external capabilities..."

That's pointing toward an agentic solution, rather 
than merely calling a language model for a simple completion.

"""
#_____fine tuning---------------------------------------
"""
One more important distinction: RAG vs fine-tuning

These are easy to confuse.

RAG
────────────────────────────
Give the model INFORMATION

"Use our company documents
to answer this question."

FINE-TUNING
────────────────────────────
Adapt MODEL BEHAVIOUR

"Make the model better suited
to a particular pattern/task."

A useful exam shortcut:

Information changes frequently or comes from company documents → think RAG.

Need to adapt learned behaviour/style/task performance → consider fine-tuning.

You don't normally fine-tune a model simply because you want it to answer from a collection of company PDFs.

"""

#text & speech------------------------------

"""
Speech synthesis     TEXT → SPEECH
Speech recognition   SPEECH → TEXT
Synthesis = create speech.
Recognition = understand/transcribe speech.
"""

"""

                 TEXT & SPEECH
                      │
        ┌─────────────┴─────────────┐
        │                           │
       TEXT                       SPEECH
        │                           │
        ├─ Sentiment                ├─ Speech recognition
        │  opinion/tone             │  SPEECH → TEXT
        │                           │
        ├─ Key phrases              ├─ Speech synthesis
        │  important topics         │  TEXT → SPEECH
        │                           │
        ├─ Named entities           └─ Speech translation
        │  person/org/place            SPEECH → other language
        │
        ├─ Language detection
        │  which language?
        │
        └─ Translation
           one language → another
"""