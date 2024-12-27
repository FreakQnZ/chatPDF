
# ChatPDF

Chat with any PDF with the power of LLM's while also changing document mid conversation and retaining conversation context to follow along in te same chat window

## Structure

```bash
    app.py
```

This has to be run to start the application

```bash
utils.py
```

This containts helper function for the main program app.py


## Run Locally

Clone the project

```bash
  git clone https://github.com/FreakQnZ/chatPDF.git
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  streamlit run app.py
```


## Environment Variables

If running this project on Ollama with locally downloaded LLM and Embeddings model no .env file is required

If HuggingFace is used we would need higging face token

`HF_TOKEN=XXXXXXXXXXX`

Additionally Langsmith for Tracing LLM calls would require

`LANGCHAIN_TRACING_V2=true`
`LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"`
`LANGCHAIN_API_KEY="XXXXXXXXXXX"`
`LANGCHAIN_PROJECT="my-app"`

