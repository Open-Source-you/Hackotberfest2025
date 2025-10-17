import streamlit as st

st.set_page_config(page_title="FAQ Chatbot Prompt Builder", page_icon="💬", layout="centered")

st.title("💬 FAQ Chatbot Prompt Builder (Free Version)")

st.write("Upload your FAQs or paste them below, then enter a question to generate a prompt for ChatGPT.")

# Business name
business_name = st.text_input("Business Name", "My Company")

# FAQ input
faq_text = st.text_area("Paste your FAQs here", height=200, placeholder="Q: What are your business hours?\nA: We are open 9am-5pm, Monday to Friday.\n...")

# Customer question
user_question = st.text_input("Customer Question", placeholder="What time do you open on Saturdays?")

if st.button("Generate Prompt for ChatGPT"):
    if faq_text.strip() and user_question.strip():
        prompt = f"You are a customer support assistant for {business_name}. Here are the FAQs:\n\n{faq_text}\n\nPlease answer this customer question based only on the FAQs above:\n\n{user_question}"
        st.success("✅ Prompt generated! Copy it and paste into ChatGPT:")
        st.code(prompt, language="text")
    else:
        st.warning("Please fill out both the FAQs and the question.")

st.markdown("---")
st.caption("💡 Tip: Paste the generated prompt into free ChatGPT at chat.openai.com.")