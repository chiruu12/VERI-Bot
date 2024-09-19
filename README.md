# VERI-Bot 📚 
[![Langchain](https://img.shields.io/badge/langchain-v0.3.0-blue)](https://github.com/hwchase17/langchain) 
[![Pinecone](https://img.shields.io/badge/pinecone-v5.1.0-yellow)](https://www.pinecone.io/) 
[![Streamlit](https://img.shields.io/badge/streamlit-v1.36.0-brightgreen)](https://streamlit.io/)

VERI-Bot is an advanced AI-powered chatbot designed to assist users by answering queries based on external data sources like PDFs, research papers, and YouTube videos. It combines natural language processing with efficient document retrieval methods to provide precise and relevant responses. The application is built using Streamlit for the user interface and leverages Pinecone for vector-based search, along with Cohere for language understanding.

## Features

- **Interactive Chat Interface**: Engage with VERI-Bot via an intuitive chat interface built using Streamlit.
- **Data Integration**: Supports PDF uploads, enabling dynamic updates to the knowledge base.
- **AI-Driven Responses**: Uses Cohere for generating contextually relevant answers based on user queries.
- **Efficient Data Retrieval**: Employs Pinecone for vector-based searching of PDFs, research papers, and more.
- **YouTube Integration**: Extracts and processes transcripts from YouTube videos to answer related questions.
- **NLP-Driven Topic Recognition**: Automatically identifies topics based on user queries to fetch the most relevant research papers.

## Technologies Used

- **Streamlit**: For building the web interface.
- **Pinecone**: For efficient vector-based document retrieval.
- **Cohere**: For generating natural language responses.
- **Langchain**: For handling document processing and chat-related utilities.
- **Python Libraries**: Includes `langchain`, `pinecone`, `cohere`, and `youtube-transcript-api` for handling various functionalities.

## How to use 

### 1. Uploading PDFs to Update Knowledge Base
Users can easily upload PDFs through the sidebar. VERI-Bot will automatically extract the content and update its knowledge base.
   
![PDF Upload Example]()

### 2. Research Paper Retrieval
You can retrieve relevant research papers based on your query using VERI-Bot's seamless integration with arXiv and Google Scholar.
   
![Research Paper Retrieval Example]()

### 3. YouTube Video Transcripts
Enter a YouTube video URL, and VERI-Bot will extract the transcript and analyze the content to answer questions.
   
![YouTube Transcript Example]()

## Getting Started
### Prerequisites

- Python 3.10+
- Docker (optional, for containerization)
- Access to Pinecone and Cohere API keys

## Installation and Setup

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/chiruu12/VERI_Bot.git
    ```

2. **Navigate to the Project Directory**:
    ```bash
    cd VERI-Bot
    ```
3. **Set up environment variables**:
    Create a `.env` file in the project root with the following content:
    ```env
    PINECONE_API_KEY=<your_pinecone_api_key>
    COHERE_API_KEY=<your_cohere_api_key>
    PINECONE_INDEX_NAME=<your_pinecone_index_name>
    ```
4. **Install Required Packages**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the Application**:
    ```bash
    streamlit run ui.py
    ```

# Using Docker to Install and Run the Application

### Prerequisites
- Make sure Docker is installed on your system. If not, [install Docker](https://docs.docker.com/get-docker/) for your operating system.

### Steps to Run the Application with Docker

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/chiruu12/VERI-Bot.git
    ```

2. **Navigate to the Project Directory**:
    ```bash
    cd VERI-Bot
    ```

3. **Build the Docker Image**:
   Ensure that the Dockerfile is located in the root directory of your project. Build the Docker image using the following command:
    ```bash
    docker build -t VERI .
    ```
    
4. **Run the Docker Container**:
   After successfully building the image, run the container using:
    ```bash
    docker run -d -p 8501:8501 VERI
    ```
   This command will:
   - Start the container in detached mode (`-d`).
   - Map port `8501` (Streamlit's default port) from the container to port `8501` on your host machine.

5. **Access the Application**:
   Open your web browser and go to: http://localhost:8501

### Usage 
1. Upload PDFs: Users can upload PDFs through the sidebar to update the chatbot's knowledge base dynamically.
2. Research Papers: Navigate to the “Research Papers” section to browse and click research paper titles, which link directly to their PDF files.
3. YouTube Integration: Extract and analyze YouTube video transcripts by entering a video URL in the “YouTube Videos” section.
4. Ask Questions: Type queries in the chat interface to receive responses based on the uploaded documents and provided data.

### NLP-Driven Topic Identification and Research Paper Retrieval
VERI-Bot uses natural language processing (NLP) to identify the topics users are querying. This process involves analyzing user queries and extracting key topics, which are then matched against research papers and documents available in the knowledge base.

To enhance the chatbot's ability to provide high-quality academic content, we integrated APIs for accessing research papers from arXiv and Google Scholar. Based on the identified topics, the system searches these databases for the most relevant papers. Only papers that meet specific criteria, such as being the most recent version (i.e., ending with "v1"), are fetched to ensure that users get the most accurate and up-to-date research material.
   
# Contributing
### Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Commit your changes (git commit -m 'Add new feature').
4. Push to the branch (git push origin feature-branch).
5. Open a Pull Request.

# License
This project is licensed under the MIT License - see the LICENSE file for details.

# Acknowledgments
- Langchain: For document processing and integration with external data.
- Pinecone: For vector-based document retrieval.
- Cohere: For generating natural language responses.
- Streamlit: For building the user interface.
- YouTube Transcript API: For extracting transcripts from YouTube videos.
- arXiv and Google Scholar: For providing access to high-quality research papers

# contact
For any questions please reach out to me at chirag.gupta.290403@gmail.com
