# AI-powered-news-search-engine 🗞️

[Pygooglenews](https://codarium.substack.com/p/reverse-engineering-google-news-rss) is a very useful usefil python library created by Artem Bugara that acts as a wrapper of the Google News RSS feed. 
the wrapper allows us to easily search for news keywords and fetch related news articles in a quick python script. 
With this library, i created an ai powered search engine that not just does regular vanilla search but is able to with the aid of embeddings created by a [pretrained sentence transformer](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) from huggingface is able to retrive very similar articles more related to the query.

Upon testing, i discovered that although ordinary vanilla searchworks fine and is on par with an embeddings similarity search for simple search queries and keywords, the ai powered search engine reigns for complex queries with relatively little lantency. A bad user experience if ever one would most likely come from the internet speed of the user as the engine attempts to retrieve relevant articles from the web

In a streamlit app, i give developed an inteface for both vanilla search and  AI-powered search and this can be run from docker hub.
Simple run 
```
docker run -d -p 8501:8501 --rm jenrola2292/ai-news-app:latest 
```
or in this repo, create a new virtual environment and pip install the requirements.txt fle then run

```
streamlit run main.py
```
You can also try out the various other sentence transformers on the huggingface model to figure out the one that makes the best search results. Finally i thought of given [FAISS](https://github.com/facebookresearch/faiss) a go but i was concerned about lantency and user experience since we would be running this on a cpu

Please reach out to me for contributions and feedback. I am always open to discussions on similarity and semantic search. 

