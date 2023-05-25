import argparse

import gradio as gr
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from prompts import QUESTION_PROMPT, COMBINE_PROMPT

parser = argparse.ArgumentParser(description='Web interface')
parser.add_argument("--persist_db_location", type=str, help="Location on disk of persisted db", default="db")
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


def submit(name):
    result = chain({"question": name})
    print(f"Answer: {result['answer']}")
    print(f"Sources: {result['sources']}")

    return result["answer"], result["sources"]


with gr.Blocks() as demo:
    question = gr.Textbox(label="Question")
    answer = gr.Textbox(label="Answer")
    sources = gr.Textbox(label="Sources")
    submit_btn = gr.Button("Submit")
    submit_btn.click(fn=submit, inputs=question, outputs=[answer, sources], api_name="submit")


demo.launch()
