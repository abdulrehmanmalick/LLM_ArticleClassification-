import time
from flask import Flask, request, session
import requests, os, json, csv
from datetime import datetime, timedelta, timezone
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from prompts import title_prompt_template, content_prompt_template
import numpy as np
import faiss
from dotenv import load_dotenv

load_dotenv()


openai_api_key = os.getenv("OPENAI_API_KEY", "")

app = Flask(__name__) 
app.secret_key = os.urandom(24)

client_id = os.getenv('INOREADER_CLIENT_ID')
client_secret = os.getenv('INOREADER_CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
csrf_protection_string = os.getenv('CSRF_PROTECTION_STRING', os.urandom(16).hex())  # Generate if not in .env
token_file = os.getenv('TOKEN_FILE')
llm1_csv_file = os.getenv('LLM1_CSV_FILE')
llm2_csv_file = os.getenv('LLM2_CSV_FILE')
tag_name = os.getenv('TAG_NAME')


specific_feeds = [
    'user/1005306036/label/OOP_Traditional media',
    'user/1005306036/label/OOP_Newsletters and feeds',
    'user/1005306036/label/OOP_Google Alerts: Data Chat Memo topics',
    'user/1005306036/label/OOP_Google Alerts: Data and Reports Calendar',
    'user/1005306036/label/OOP_Google Alerts: OOP Priority Topics',
    'user/1005306036/label/K-12 Education (Manually Curated)'
]

processed_article_ids = set()

all_articles_ids = set()
llm1_article_ids = set()
llm2_article_ids = set()

# Step 1: Load Titles and Create FAISS Index with Docstore
def create_embeddings_from_csv(csv_file):
    titles = []
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            titles.append(row[0])
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
    embeddings = embedding_model.embed_documents(titles)
    return titles, np.array(embeddings)

def initialize_faiss_index(embeddings, titles):
    # Initialize the FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Create an empty InMemoryDocstore
    docstore = InMemoryDocstore({i: {"page_content": title} for i, title in enumerate(titles)})
    
    # Create the FAISS vector store
    vector_store = FAISS(
        embedding_function=OpenAIEmbeddings(model="text-embedding-3-large"),
        index=index,
        docstore=docstore,
        index_to_docstore_id={i: i for i in range(len(titles))}
    )
    
    return vector_store

# Create embeddings and initialize FAISS with your CSV file
titles, embeddings = create_embeddings_from_csv('YesTitles.csv')
vector_store = initialize_faiss_index(embeddings, titles)

# Existing helper functions remain unchanged
def save_tokens(tokens):
    with open(token_file, 'w') as f:
        json.dump(tokens, f)

def load_tokens():
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            return json.load(f)
    return None

def refresh_access_token(refresh_token):
    token_url = "https://www.inoreader.com/oauth2/token"
    data = {
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(token_url, data=data, headers=headers)
    if response.status_code == 200:
        tokens = response.json()
        save_tokens(tokens)
        return tokens['access_token']
    return None

def save_to_csv(article, filename, fieldnames, article_set):
    try:
        article_id = article['id']
        if article_id in article_set:
            print(f"Skipping already processed article: {article_id} for file: {filename}")
            return
        
        print(f"Attempting to save article ID {article_id} to file: {os.path.abspath(filename)}")
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0: 
                writer.writeheader()
            filtered_article = {field: article.get(field, '') for field in fieldnames}
            writer.writerow(filtered_article)
        
        article_set.add(article_id)
        print(f"Article ID {article_id} successfully saved to {filename}")
    except PermissionError as e:
        print(f"PermissionError: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def save_llm1_output_to_csv(article, filename):
    fieldnames = ['id', 'title', 'timestamp', 'content', 'feed'] 
    save_to_csv(article, filename, fieldnames=fieldnames, article_set=llm1_article_ids)

def save_llm2_output_to_csv(article, filename):
    fieldnames = ['id', 'title', 'timestamp', 'content', 'feed'] 
    save_to_csv(article, filename, fieldnames=fieldnames, article_set=llm2_article_ids)

def tag_article_as_k12_education(access_token, article_id, tag_name):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'i': article_id,
        'a': tag_name
    }
    response = requests.post('https://www.inoreader.com/reader/api/0/edit-tag', headers=headers, data=data)
    if response.status_code != 200:
        print(f"Error tagging article {article_id}: {response.text}")

def fetch_with_retries(url, headers, params, max_retries=5):
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response
        elif response.status_code == 429:
            reset_time = int(response.headers.get("X-Reader-Limits-Reset-After", 60))
            print(f"Rate limit hit. Retrying in {reset_time} seconds...")
            time.sleep(reset_time)
        else:
            print(f"Error fetching data: {response.status_code} - {response.content}")
            break
    return None

@app.route('/')
def home():
    auth_url = f"https://www.inoreader.com/oauth2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=read write&state={csrf_protection_string}"
    return f'Go to <a href="{auth_url}">this URL</a> to authorize the app.'

@app.route('/callback')
def callback():
    state = request.args.get('state')
    if state != csrf_protection_string:
        return 'Error: Invalid state parameter.'

    code = request.args.get('code')
    token_url = "https://www.inoreader.com/oauth2/token"
    data = {
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'your-user-agent'
    }
    response = requests.post(token_url, data=data, headers=headers)
    tokens = response.json()

    if 'access_token' in tokens:
        save_tokens(tokens)
        session['access_token'] = tokens['access_token']
        session['refresh_token'] = tokens['refresh_token']
        session['expires_in'] = tokens['expires_in']
        return f'Access token: {tokens["access_token"]}<br>Refresh token: {tokens["refresh_token"]}<br>Expires in: {tokens["expires_in"]} seconds'
    else:
        return f'Error: {tokens.get("error", tokens)}'

@app.route('/all-articles')
def all_articles():
    tokens = load_tokens()
    if not tokens or 'access_token' not in tokens:
        return 'Error: Missing access token.'

    access_token = tokens['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    
    now = datetime.now(timezone.utc)
    oldest_timestamp = int((now - timedelta(days=7)).timestamp())
    newest_timestamp = int(now.timestamp())

    article_count = 0 
    total_api_requests = 0

    for feed in specific_feeds:
        # Set up parameters to fetch 50 articles per feed
        params = {
            'n': 100,
            'output': 'json',
            'ot': oldest_timestamp,
            'nt': newest_timestamp
        }
        
        response = fetch_with_retries(f'https://www.inoreader.com/reader/api/0/stream/contents/{feed}', headers, params)
        if response is None:
            print(f"Failed to fetch articles for feed: {feed}")
            continue
        
        total_api_requests += 1

        items = response.json().get('items', [])
        print(f"Fetched {len(items)} articles from feed: {feed}")

        for item in items:
            process_article(item, access_token, feed)

    print(f"Total API requests: {total_api_requests}")
    return {
        'message': f'Articles fetched and saved. Total API requests: {total_api_requests}'
    }

def process_article(item, access_token, stream):
    article_id = item['id']
    
    # Check early if the article has already been processed
    if article_id in processed_article_ids:
        print(f"Skipping already processed article: {article_id}")
        return  # Skip articles that are already processed early
    
    article = {
        'id': article_id,   
        'title': item.get('title', 'No Title'),
        'timestamp': item['published'],
        'content': item.get('summary', {}).get('content', ''),
        'feed': stream 
    }

    save_to_csv(article, 'all_articles.csv', ['id', 'title', 'timestamp', 'feed', 'content'], all_articles_ids)

    llm1_result = check_title_with_llmsimilarity(article['title'])
    print(f"LLM1 Result: {llm1_result}")

    if llm1_result == 'yes':
        print(f"Article passed LLM1: {article['title']}")
        save_llm1_output_to_csv(article, llm1_csv_file)
        processed_article_ids.add(article_id)

        llm2_result = check_content_with_llm2(article['content'])
        print(f"LLM2 Result: {llm2_result}")
        
        if llm2_result == 'yes':
            print(f"Article passed LLM2: {article['title']}")
            save_llm2_output_to_csv(article, llm2_csv_file)
            tag_article_as_k12_education(access_token, article_id, tag_name)
        else:
            print(f"Article did not pass LLM2: {article['title']}")
    else:
        print(f"Article did not pass LLM1: {article['title']}")


def check_title_with_llmsimilarity(title):
    # Check for semantic similarity using the vector store first
    print(f"Checking title: {title}")  # Debug: Log the title being checked
    
    title_embedding = np.array(vector_store.embedding_function.embed_query(title))
    distances, indices = vector_store.index.search(title_embedding.reshape(1, -1), k=1)
    
    print(f"Distances: {distances}")  # Debug: Log the distances returned by FAISS
    print(f"Indices: {indices}")  # Debug: Log the indices of similar titles
    
    # If a close match is found, bypass LLM1 and pass directly to LLM2
    if distances[0][0] < 0.5:  # Adjust this threshold based on your needs
        similar_titles = [titles[idx] for idx in indices[0]]
        print(f"Similar titles from vector store: {similar_titles}")  # Debug: Log similar titles
        return 'yes'
    
    # If no similar titles found, fallback to LLM1 check
    print(f"No similar title found, falling back to LLM1.")  # Debug: Log fallback to LLM1
    
    prompt = PromptTemplate(input_variables=["input"], template=title_prompt_template)
    llm = ChatOpenAI(model="gpt-4o-2024-08-06", temperature=0.7)
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"input": title})
    response = response.strip().lower()
    print(f"LLM1 Response: {response}")  

    if 'yes' in response:
        return 'yes'
    else:
        return 'no'

def check_content_with_llm2(content):
    print("Content being evaluated by LLM2:", content[:500])
    prompt_content = PromptTemplate(input_variables=["input"], template=content_prompt_template)
    llm_content = ChatOpenAI(model="gpt-4o-2024-08-06")
    chain_content = prompt_content | llm_content | StrOutputParser()

    response = chain_content.invoke({"input": content})
    response = response.strip().lower()

    print(f"LLM2 Response: {response}")

    if 'yes' in response:
        return 'yes'
    else:
        return 'no'

if __name__ == '__main__':
    app.run(port=8000, debug=True)