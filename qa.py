import argparse

from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from prompts import QUESTION_PROMPT, COMBINE_PROMPT

parser = argparse.ArgumentParser(description='Ask a question')
parser.add_argument('question', type=str, help='The question to ask')
parser.add_argument("--persist_db_location", type=str, help="Location on disk to persist the db", default="db")
args = parser.parse_args()

# Load the LangChain.
embedding = OpenAIEmbeddings()
store = Chroma(persist_directory=args.persist_db_location, embedding_function=embedding)
retriever = store.as_retriever(search_type="mmr")

chain = RetrievalQAWithSourcesChain.from_llm(
    llm=OpenAI(temperature=0),
    question_prompt=QUESTION_PROMPT,
    combine_prompt=COMBINE_PROMPT,
    retriever=retriever)

result = chain({"question": args.question})
print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")
