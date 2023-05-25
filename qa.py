"""Ask a question to the notion database."""
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI, PromptTemplate
from langchain.chains import VectorDBQAWithSourcesChain, RetrievalQAWithSourcesChain
import argparse

from prompts import QUESTION_PROMPT, COMBINE_PROMPT

parser = argparse.ArgumentParser(description='Ask a question')
parser.add_argument('question', type=str, help='The question to ask')
args = parser.parse_args()

# Load the LangChain.
PERSIST_DIRECTORY = "db"

embedding = OpenAIEmbeddings()
store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embedding)
retriever = store.as_retriever(search_type="mmr")
# chain = RetrievalQAWithSourcesChain.from_llm(
#     llm=OpenAI(temperature=0),
#     question_prompt=QUESTION_PROMPT,
#     combine_prompt=COMBINE_PROMPT,
#     retriever=retriever
# )
chain = RetrievalQAWithSourcesChain.from_llm(
    llm=OpenAI(temperature=0),
    question_prompt=QUESTION_PROMPT,
    combine_prompt=COMBINE_PROMPT,
    retriever=retriever)

result = chain({"question": args.question})
print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")
