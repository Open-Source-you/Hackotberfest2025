
    )
    # Linking the LLM, vector DB and the prompt
    docs_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vector_store.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, docs_chain)
    return retrieval_chain

number = int(input("Do you want me to:\n 1) Learn from a single article \n 2) Learn from articles of a given topic\n :"))
if (number == 2):
    topic = input("What topic to do you want me to learn?: ")
    results = wiki.search(topic)
    for result in results:
    	wiki_url = str("https://en.wikipedia.org/wiki/"+str(result)).replace(' ','_')
    	chain = create_RAG_model(wiki_url, "dolphin-phi")
elif (number == 1):
    wiki_url = input("Give me the URL of the article: ")
    chain = create_RAG_model(wiki_url, "dolphin-phi")

print("Type 'exit' to exit")

while True:
    query = input("Ask me a question: ")
    if (query == "exit"):
        break
    else:
        output = chain.invoke({"input":query})
        print(output["answer"])
