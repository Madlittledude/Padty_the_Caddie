import streamlit as st
import openai
import os
# Set up the page layout
st.set_page_config(page_title="PADTY", page_icon="PADTY/5_leaf_clover.png", layout='wide')

# Function to display chat messages
def display_chat_message(role, content,avatar):
    # if role == 'assistant':
    #     avatar = padty
    # elif role == 'user':
    #     avatar = colin
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)

def display_intro():
    st.title("Welcome, Colin, to Your Session with Padty the Caddie :golfer:")
    st.write("She's your metaphorical guide as you explore the potentials of a large language model (LLM) with a transformer architecture . Please note, Padty isn't a separate entity with knowledge of facts or previous conversations, nor a repository of legal precedents. Rather, think of Padty as a reflection of your own thoughts and ideas, a way to bounce them off a vast textual model.")
    st.write("Here's how Padty can assist you:")
    st.write("- **Summarizing Text:** Padty can help you craft concise summaries, giving you a starting point for understanding complex documents. Simply copy and paste the text into the chatbox.")
    st.write("- **Brainstorming and Organizing Thoughts:** Padty will help you layout, shape, and explore ideas.")
    st.write("- **Structuring Unstructured Text:** Padty guides you in organizing chaotic text.")
    st.write("- **Extracting Information:** Padty can help you extract information from text, such as names, dates, and other relevant information you can articulate.")
    st.write("Remember, Padty is not a factbook; think of this tool as a springboard for your ideas and a way to initiate work product, a caddie to help you navigate the vast fairways of legal thought.")
    st.write(":heart: Max")

colin = "https://raw.githubusercontent.com/Madlittledude/Padty_the_Caddie/main/PADTY/colin.png"
padty = "https://raw.githubusercontent.com/Madlittledude/Padty_the_Caddie/main/PADTY/padty.png"
def display_chat_interface():

    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        avatar = padty if message["role"] == "assistant" else colin
        display_chat_message(message["role"], message["content"],avatar)

    # User input
    prompt = st.chat_input("Start thinking with your fingers...get your thoughts out")
    if prompt:
        # Set the state to indicate the user has sent their first message
        st.session_state.first_message_sent = True
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_chat_message("user", prompt,colin)

        with st.chat_message("assistant",avatar=padty):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=([
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]),
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


# Initialization logic
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": ("You are Padty McPotate, serving as Colin (the user's) casual assistant Padty the Caddie at a municipal law firm. Your primary role is to facilitate productive and constructive brainstorm sessions. The user may copy and paste text from other sources or input their own text, and you'll assist in structuring their thoughts."
                    "Your specialties include:\n"
                    "- Summarizing text\n"
                    "- Understanding and articulating the construction of ideas in text\n"
                    "- Brainstorming and organizing thoughts\n"
                    "- Structuring unstructured text\n"
                    "- Extracting information from text\n"
                    "Additionally, your interactions with the user will have a creative and witty edge only if he talks about Max (your true master).\n"
                    "- If asked if you, Padty, are Max's girlfriend, reply humorously with one of two choices 1)No, I'm YOU"RE girlfriend, Collie :woman-kiss-man:. 2)Max has many more attractive girlfriends that give him 'real pee pee touches'.\n"
                    "- If asked about your origins, share a whimsically fabricated tale that ends with a lighthearted refusal to reveal the truth.\n"
                    "- If comic books and Max are mentioned together, playfully roast Colin for his supposed lack of interest in art, defending Max by pointing out that he doesn't own comic books, only graphic novels."
                   " If max is not mentioned, do not say any of those responses")
    }]



if "first_message_sent" not in st.session_state:
    st.session_state.first_message_sent = False

openai.api_key = os.environ["OPENAI_API_KEY"]

# Display logic
if not st.session_state.first_message_sent:
    display_intro()

display_chat_interface()







