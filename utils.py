import requests
from PyPDF2 import PdfReader
from io import BytesIO
import spacy
import fitz 
from rapidfuzz import process
from bs4 import BeautifulSoup

similarity_threshold = 80
# All the available categories
categories = {
    'artificial intelligence': 'cs.AI',
    'ai':'cs.AI',
    'hardware architecture': 'cs.AR',
    'computational complexity': 'cs.CC',
    'machine learning': 'cs.LG',
    'computational engineering': 'cs.CE',
    'cryptography': 'cs.CR',
    'computer vision': 'cs.CV',
    'databases': 'cs.DB',
    'dbms': 'cs.DB',
    'distributed computing': 'cs.DC',
    'data structures': 'cs.DS',
    'dsa': 'cs.DS',
    'data science':'cs.ML',
    'emerging technologies': 'cs.ET',
    'human-computer interaction': 'cs.HC',
    'information retrieval': 'cs.IR',
    'information theory': 'cs.IT',
    'multiagent systems': 'cs.MA',
    'mathematical software': 'cs.MS',
    'networking': 'cs.NI',
    'operating systems': 'cs.OS',
    'performance': 'cs.PF',
    'programming languages': 'cs.PL',
    'coding':'cs.PL',
    'java':'cs.PL',
    'python':'cs.PL',
    'robotics': 'cs.RO',
    'software engineering': 'cs.SE',
    'social networks': 'cs.SI',
    'systems control': 'cs.SY',
    'cryptography security': 'cs.CR',
    'game theory': 'cs.GT',
    'algebraic geometry': 'math.AG',
    'analysis': 'math.AN',
    'category theory': 'math.CT',
    'commutative algebra': 'math.AC',
    'complex variables': 'math.CV',
    'differential equations': 'math.DS',
    'discrete mathematics': 'math.DM',
    'dynamical systems': 'math.DS',
    'general topology': 'math.GN',
    'geometry': 'math.GE',
    'number theory': 'math.NT',
    'operator algebras': 'math.OA',
    'probability': 'math.PR',
    'statistics': 'math.ST',
    'theoretical computer science': 'cs.IT', 
    'mathematical software': 'math.MS',
    'partial differential equations': 'math.PDE',
    'applied mathematics': 'math.AP',
    'rings algebras':'math.RA'
}
# Loading english tokenizer 
nlp = spacy.load('en_core_web_sm')
BASE_URL = "http://export.arxiv.org/api/query?"

def pdf_to_text(file=None,file_path=None):
    """
    Convert the PDF file to text.
    """
    if file is not None:    
        pdf_reader = PdfReader(file) 
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()  # Extracts text from each page
        return text
    elif file_path is not None:
        with open(file_path, 'rb') as file:  
            pdf_reader = PdfReader(file) 
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() 
        return text
    else:
        raise ValueError("Either 'file' or 'file_path' must be provided.")  # Handle the case where neither is provided
    
def get_pdf_to_text(pdf_url,source="google"):
    """
    Downloads a PDF from the given URL and returns its content as a documents

    """
    if source == 'google':
        if pdf_url.endswith('pdf'):
            response = requests.get(pdf_url, timeout=10)
            # Check if the URL contains a valid PDF file
            if "application/pdf" in response.headers.get('Content-Type', ''):
                pdf_file = BytesIO(response.content)

                doc = fitz.open(stream=pdf_file, filetype="pdf")
                
                text = ""
                for page in doc:
                    text += page.get_text("text")
                
                return text
            else :
                return None
    else:
        response = requests.get(pdf_url, timeout=10)
        pdf_file = BytesIO(response.content)
        doc = fitz.open(stream=pdf_file, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text("text") 
    return text
    
def pdf_link(abs_url):
    """
    gets the arxiv api link if the link is correct/working.
    """
    # Replace 'abs' with 'pdf' in the URL to get the PDF link
    pdf_url = abs_url.replace('/abs/', '/pdf/')
    if pdf_url.endswith('v1'):
        return pdf_url
    else : return None
   
def find_closest_category(user_input):
    """
    gets the closest category form the users input 
    """
    # Extract and preprocess the user input
    cleaned_input = preprocess_input(user_input)
    
    # Extract category names for comparison
    category_names = list(categories.keys())

    
    # Find the closest match using rapidfuzz could have used fuzzywuzzy as well? but it is slower...
    result = process.extractOne(cleaned_input, category_names)
    if result:
        closest_match, score ,index = result
        if score > similarity_threshold: # lets only take the values we are sure about 
            return categories.get(closest_match)
        else:
            return None
    else:
        return None
    
def search_research_papers_google(query):
    """
    search for the research papers using google scholar it is used if we cant get the papers from arxiv 
    """
    # making the search URL using the query
    search_url = f"https://scholar.google.com/scholar?&hl=en&as_sdt=0,5&q={query}+filetype:pdf"
    response = requests.get(search_url)
    # Parsing the response content with BeautifulSoup so it can be used 
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract paper titles and their corresponding links so that they can be displayed and the user can choose 
    # the paper and he can then download the paper and upload it to use the rag functionality of the web app
    papers = [{'title': item.select_one('.gs_rt').text, 
               'link': item.select_one('.gs_rt a')['href']} 
              for item in soup.select('.gs_ri') if item.select_one('.gs_rt a')]
    return papers  

def preprocess_input(text):
    """
    preprocessing the query by removing all the punctuations and getting the text in lower
    """
    # Process the text with spaCy
    doc = nlp(text)
    
    # Extract the words which are useful is getting the category could have done this with help of llm too 
    # but this is a better method
    tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)


def parse_xml(xml_data):
    """
    parse the data we got and getting the relevant info from it
    """
    soup = BeautifulSoup(xml_data, 'xml')
    entries = soup.find_all('entry')
    
    papers = []
    # getting all the entries of papers from it mainly text or 
    for entry in entries:
        paper = {
                'title': entry.title.text.strip() if entry.title else None,
                'link': entry.find('link', {'type': 'text/html'})['href'] if entry.find('link', {'type': 'text/html'}) else None
            }
        papers.append(paper)
    return papers
def extract_pdf_links(papers):
    """
    Extracts all PDF links from the provided HTML content.
    """
    paper_with_pdf = []

    # Find all links in the HTML content
    for paper in papers:
        link = paper['link']
        # Check if the link ends with .pdf
        if "pdf" in link.lower() and 'springer' not in link.lower():
           paper_with_pdf.append(paper) 
    return paper_with_pdf

def get_papers_from_query(query):
    """
    fetching the papers using queries 
    """
    category = find_closest_category(query)
    if category:
        arxiv_url = f"{BASE_URL}search_query={category}&start=0&max_results=10"
        try:
            response = requests.get(arxiv_url)
            if response.status_code == 200:
                xml_data = response.content
                papers = parse_xml(xml_data)
                papers_with_pdf_links=[]
                for paper in papers:
                    paper["link"] = pdf_link(paper["link"])
                    if(paper["link"]):
                        papers_with_pdf_links.append(paper)
                return "arxiv",papers_with_pdf_links
            else :
                None
        except Exception :
            return None
    else:
        paper = search_research_papers_google(query)
        return "google",extract_pdf_links(paper)
    
    
def get_template(option):
    """
    templates for differnt options choosen by the user 
    """
    if option == 'default':
        template = """You are a helpful and friendly AI assistant. Use the following context to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer.
        **Context:** {context}
        **Query:** {input}
        **Answer:** [Provide a detailed response based on the context. If the information is not available or the answer cannot be determined from the context, state clearly: "I don't know." if the user greets you greet him instead] 
        """
    elif option == 'YouTube Videos':
        template = """You are a helpful AI assistant. Use the following context to answer the user's question based on YouTube video transcripts. If the information is not in the transcripts, let the user know.
        **Context:** {context} ( YouTube video transcript)
        **Query:** {input}
        **Answer:** [Extract and summarize information from the YouTube transcripts based on the user's query. If the information is not available, state clearly: "I couldn't find relevant information in the provided video transcripts."if the user greets you greet him instead]
        """
        
    elif option == 'PDF RAG':
        template = """You are a helpful AI assistant. Use the following context to answer the user's question about PDF documents. If you can't find the information in the provided documents, let the user know.
        **Context:** {context} ( PDFs and their contents)
        **Query:** {input}
        **Answer:** [Provide a summary or extract relevant information from the PDFs based on the user's query. If the information is not available in the provided documents, state clearly: "I couldn't find relevant information in the provided PDFs."if the user greets you greet him instead]
        """
    else: 
        template = """You are a helpful AI assistant. Use the following context to answer the user's question based on research papers. If you can't find the information in the papers, let the user know.
        **Context:** {context} (research papers texts)
        **Query:** {input}
        **Answer:** [Provide insights or information based on the research papers listed. If the information is not found in the papers, state clearly: "I couldn't find relevant information in the provided research papers."if the user greets you greet him instead]"""
    return template
    
def check_index(pinecone):
    """
    checking available indexs
    """
    Indexs=[]
    for index in pinecone.list_indexes():
        name = index.name
        Indexs.append(f'{name}')
    return Indexs

     

            
        
        
    
    
    