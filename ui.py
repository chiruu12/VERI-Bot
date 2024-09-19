
import streamlit as st
from streamlit_option_menu import option_menu
from rag_chain import RAG_Chain
import requests
# Streamlit page configuration
st.set_page_config(page_title='VERI', layout='wide', initial_sidebar_state='expanded')

# Custom CSS styling
st.markdown("""
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #000000;
            color: #E0E0E0; 
        }

        .stSidebar {
            background-color: #2C2C2C; 
        }
        .sidebar-emoji img {
            width: 2in; 
            height: 2in;
            top: -40px;
            position: absolute;
        }
        .main-container {
            background-color: #211d21;
            border: 5px solid transparent; 
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            position: relative;
            top: -20px; 
            z-index: 1;
            /* Rainbow border effect */
            background: linear-gradient(#211d21, #211d21) padding-box,
                        linear-gradient(45deg, red, orange, yellow, green, blue, indigo, violet, red) border-box;
        }
        .heading-title {
            font-size: 32px; 
            font-weight: bold;
            color: #c10206;
            text-align: left;
            margin-bottom: 10px;
        }

        .instructions {
            font-size: 16px;
            color: #E8E8E8; 
            line-height: 1.6; 
        }
    </style>
""", unsafe_allow_html=True)


#combined heading and instructions box
st.markdown('''
    <div class="main-container">
        <div class="heading-title">📚 Virtual Education & Research Intelligence Bot</div>
        <div class="instructions">
            <h3>Instructions:</h3>
            <ul>
                <li>Select feature depending on your needs:
                    <ul>   
                        <li>PDFs: Upload and extract information from PDFs.</li>
                        <li>Research Papers: Search for and analyze academic papers.</li>
                        <li>YouTube Videos: upload the link of the video and then extract information from it </li>
                    </ul>
                </li>
                <li>You can either upload a PDF file or enter a link to a document. The bot will assist in processing and analyzing the content.</li>
                <li>Use the provided options or enter a topic you want to study. The bot will help you with YouTube videos, research papers, or PDFs based on your input</li>
                <li>Type your query or request in the chat input field.</li>
                <li>To clear the conversation, click the 'Clear Chat' button in the sidebar.</li>
            </ul>
        </div>
    </div>
''', unsafe_allow_html=True)

st.sidebar.markdown(
    """
    <div style="margin-bottom: 20px;">
        <img src="https://em-content.zobj.net/source/microsoft-teams/363/teacher-light-skin-tone_1f9d1-1f3fb-200d-1f3eb.png" width="180" height="180" />
    </div>
    """,
    unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state.messages = []
    
if 'option' not in st.session_state:
    st.session_state['option'] = 'none'
with st.sidebar:
    selected = option_menu(
        "VERI-Bot",
        ["Home", "PDF RAG", "Research Papers", "YouTube Videos"],
        icons=["house", "file-earmark-pdf", "book", "youtube"],
        default_index=0,
        styles={
            "container": {"padding": "5px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#4CAF50"},
        }
    )
    
def main():
    rag_chain = RAG_Chain(option=selected)
    chain = rag_chain.get_rag_chain()
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if selected == "PDF RAG":
        uploaded_file = st.sidebar.file_uploader("Upload a PDF resume", type="pdf")
        if st.session_state.option:
            if uploaded_file :
                rag_chain.update_vectorstore_with_files(uploaded_file)
                rag_chain.change_template(selected)
                chain = rag_chain.get_rag_chain()
                
    elif selected == "Research Papers":
        category = st.sidebar.text_input("Enter the subject")
        if st.session_state.option:
            if category:
                papers=rag_chain.update_vector_store_with_research_papers(category)
                rag_chain.change_template(selected)
                chain = rag_chain.get_rag_chain()
                for paper in papers:
                    st.sidebar.markdown(f"[{paper['title']}]({paper['link']})")
    elif selected == "YouTube Videos":
        video_link = st.sidebar.text_input("Enter video link")
        if st.session_state.option:
            if video_link:
                try:
                    response = requests.head(video_link, timeout=5)
                    if response.status_code == 200:
                        rag_chain.update_vector_store_with_youtube(video_link)
                        rag_chain.change_template(selected)
                        chain = rag_chain.get_rag_chain()

                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    
                    
                    
    if query:= st.chat_input("Please ask your Query?"):
        st.session_state.messages.append({"role": "user", "content": query})  # Add user query to session state(messages)
        with st.chat_message("user"):
            st.markdown(query)  # Display user query
            
        with st.chat_message("assistant") and st.spinner('Processing...'):
            try:
                response = chain.invoke({"input": query})
                answer = response["answer"]  # only getting the answer from the response as it is a dictionary  
                response = st.write(answer) 
                st.session_state.messages.append({"role": "assistant", "content": answer}) # Add assistant's answer to session state(messages)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        
        
if st.sidebar.button("Clear Chat", key="clear_chat", help="Clear conversation history"):
    st.session_state.messages = []
    
if __name__ == "__main__":
    main()




