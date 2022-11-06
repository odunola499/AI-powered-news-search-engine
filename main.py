import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer
from py_news import GoogleNews
from sentence_transformers.util import cos_sim
from newspaper import Article


st.set_page_config(
    page_title = "ML Powered News Engine",
    page_icon = "🗞️",
    layout = "wide"
)



class Engine:
    def __init__(self,encoding_model = 'sentence-transformers/msmarco-distilbert-base-tas-b'):
        self.embedding_model = SentenceTransformer(encoding_model)
        self.stopwords = set(stopwords.words('english'))
        self.tokenize = word_tokenize
        self.gn = GoogleNews()
    def clean_query(self):
        tokens = set(self.tokenize(self.input))
        return tokens - self.stopwords
    def get_search_results_dict(self):
        tokens = self.clean_query()
        self.results = dict()
        result = self.gn.search(self.input)['entries'][:10]
        for news in result:
                self.results[news['title']] = news['link'] 
        for token in tokens:
            result = self.gn.search(token)['entries'][:5]
            for news in result:
                self.results[news['title']] = news['link'] 
        return self.results
    def embed(self):
        results = self.get_search_results_dict()
        sentences = list(results.keys())
        context = self.embedding_model.encode(sentences)
        query = self.embedding_model.encode(self.input)
        return query, context, sentences, results

    def compute_similarity(self):
        query, context, sentences, results = self.embed()
        scores = cos_sim(query, context)
        scores = scores.numpy()[0]
        sorted_sentences = [y for x,y in sorted(zip(scores, sentences), reverse = True)][:10]
        links = []
        for i in sorted_sentences:
            links.append(results[i])

        return sorted_sentences[:10], links
    def design(self):
        sentences, results = self.compute_similarity()
        for i in sentences:
            st.markdown(f'#### {i}')
    def get_summaries(self):
        sentences, results = self.compute_similarity()
        articles = []
        for sen in sentences:
            link = results[sen]
            text = self.get_text(link)
            articles.append(text)
        
        summaries = self.pipe(articles)
        return summaries

    def get_text(self,link):
        a = Article(link)
        a.download()
        a.parse()
        return a.text
    
    def vanilla_search(self):
        result = self.gn.search(self.input)['entries'][:10]
        links = []
        headlines = []
        for news in result:
                headlines.append(news['title'])
                links.append(news['link'])
        return headlines, links
    def run(self, query):
        self.input = query
        return self.compute_similarity()
    def vanilla_run(self, query):
        self.input = query
        return self.vanilla_search()
engine = Engine()
st.subheader('News Search Engine')
input = st.text_input('type query here')

with st.sidebar:
    search_type = st.radio("Please choose preferred search type",
                            ('vanilla search', 'AI-powered search'))

if st.button('Go') or input:
    if search_type == 'vanilla search':
        with st.spinner('searching...'):
            sentences, links = engine.vanilla_run(input)
            for i,j in zip(sentences, links):
                st.markdown(f'### {i}')
                st.markdown(f'[click here to visit]({j})')
    else:
        with st.spinner('searching...'):
            sentences, links = engine.run(input)
            for i,j in zip(sentences, links):
                st.markdown(f'### {i}')
                st.markdown(f'[click here to visit]({j})')

