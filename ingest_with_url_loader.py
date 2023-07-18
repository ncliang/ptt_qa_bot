import argparse
import re

import requests
from bs4 import BeautifulSoup
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

parser = argparse.ArgumentParser(description='Ingest information from PTT posts')
parser.add_argument("--board_name", type=str, help="Name of board to ingest", default="Japan_Living")
parser.add_argument("--num_list_pages", type=int, help="Number of list pages to ingest", default=10)
parser.add_argument("--persist_db_location", type=str, help="Location on disk to persist the db", default="db")

args = parser.parse_args()


BASE_URL = "https://www.ptt.cc"
LIST_PAGE = BASE_URL + "/bbs/" + args.board_name + "/index.html"
LIST_PAGE_TEMPLATE = BASE_URL + "/bbs/" + args.board_name + "/index%d.html"
POST_PAGE_PATH_PATTERN = re.compile(r".*\/M\.\d+\.A\.[0-9A-Za-z]+\.html")
INDEX_PAGE_PATH_PATTERN = re.compile(r".*\/index(\d+)\.html")
PREVIOUS_PAGE = "上頁"


def find_index_range():
    resp = requests.get(LIST_PAGE)
    assert resp.ok

    soup = BeautifulSoup(resp.text, 'html.parser')
    a_elements = soup.find_all('a')
    previous_page_a_elements = [e for e in a_elements if PREVIOUS_PAGE in e.text]
    assert len(previous_page_a_elements)

    previous_page_a_element = previous_page_a_elements[0]
    previous_page_path = previous_page_a_element.get("href")
    m = INDEX_PAGE_PATH_PATTERN.match(previous_page_path)
    assert m
    prev_index_num = int(m.group(1))

    last_index_num = prev_index_num + 1
    first_index_num = max(last_index_num - args.num_list_pages, 0)
    print("Processing list pages %d to %d" % (first_index_num, last_index_num))
    return range(last_index_num, first_index_num, -1)


INDEX_RANGE = find_index_range()

print("Compiling urls from list pages in range %d to %d" % (INDEX_RANGE.stop, INDEX_RANGE.start))
urls = []
for idx in INDEX_RANGE:
    list_page = LIST_PAGE_TEMPLATE % idx
    resp = requests.get(list_page)
    assert resp.ok

    soup = BeautifulSoup(resp.text, 'html.parser')
    a_elements = soup.find_all('a')
    for a_element in a_elements:
        post_page_path = a_element.get("href")
        if not post_page_path:
            continue
        m = POST_PAGE_PATH_PATTERN.match(post_page_path)
        if m:
            urls.append(BASE_URL + post_page_path)

print("Compiled %d urls" % len(urls))

print("Loading URLs")
loader = UnstructuredURLLoader(urls=urls)
documents = loader.load()

print("Splitting documents")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
texts = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")
# embeddings = OpenAIEmbeddings()

print("Creating vectorstore")
db = Chroma.from_documents(texts, embeddings, persist_directory=args.persist_db_location)

print("Persisting vectorstore")
db.persist()
