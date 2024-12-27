from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

def ingestion(pdf):
    loader = PyPDFLoader(pdf)
    document = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separator="\n")
    texts = text_splitter.split_documents(document)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vectorstore = FAISS.from_documents(
        texts,
        embeddings
    )

    return vectorstore

def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

def RagChain(query, vectorstore, chat_history):

    if chat_history == []:
        chat_history = "No chat history"

    chat_history_dict = {"history": chat_history}

    llm = ChatOllama(
        model="llama3.2",
        temperature=0.2
    )

    template = """
    Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Try to explain the answer in 3-4 sentences keeping it to the point
    You are also given the chat history where assistant is your answer and Human is the query, Use this to understand the chronoligical context
    Always say "thanks for asking!" at the end of the answer.

    <history>
    {history}
    </history>

    <context>
    {context}
    </context>

    Question: {question}

    Helpful Answer:
    """

    prompt = PromptTemplate(template=template)

    retriever = vectorstore.as_retriever()

    retrieval_chain = (
        {
            "context" : retriever | format_docs ,
            "history" : RunnablePassthrough() | (lambda _: chat_history) ,
            "question" : RunnablePassthrough()
        }
        | prompt
        | llm
    )

    res = retrieval_chain.invoke(input=query)
    return res
