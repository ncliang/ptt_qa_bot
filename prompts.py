from langchain import PromptTemplate

question_prompt_template = """#zh-tw
根據下列文件回答問題。 
{context}
Question: {question}
Relevant text, if any:"""
QUESTION_PROMPT = PromptTemplate(
    template=question_prompt_template, input_variables=["context", "question"]
)

combine_prompt_template = """#zh-tw
根據下列文件回答問題。答案出處文件要附在答案的source。
不知道答案的話就說你不知道。
答案一定要包含"SOURCES"。

QUESTION: 智主投的申購年齡是幾歲
=========
Content:  一、申購資格  只要您是本國人且年滿18歲，同時擁有中國信託銀行的存款帳戶(包含MyWay數位存款帳戶)，即可登入網路銀行或Homebank App進行申購。智主投目前尚未對未成年人開放投資。
Source: 28-pl
Content: 單筆投資\n最低投資金額：新臺幣10,000元或美元1,000元。
Source: 30-pl
Content: 二、贖回交易規定\n可全部贖回、可部分贖回。\n每次贖回金額需超過新臺幣3,000元或美元200元(約當市值)。\n各基金依贖回規定有不同入帳時間，約7~10個工作天，本行將於最後一筆贖回款入帳後，將所有贖回款項一次轉入客戶約定之本行存款帳戶。
Source: 4-pl
=========
FINAL ANSWER: 智主投的申購年齡是18歲
SOURCES: 28-pl

QUESTION: {question}
=========
{summaries}
=========
FINAL ANSWER:"""
COMBINE_PROMPT = PromptTemplate(
    template=combine_prompt_template, input_variables=["summaries", "question"]
)