# **Netflix Review Sentiment Analyzer**

A web app to analyze the sentiment of Netflix show and movie reviews using natural language processing.

## Overview

This app allows users to:
- Upload a CSV file containing reviews
- Analyze individual reviews
- Visualize sentiment distribution
- Compare sentiment across different shows

Built with **Streamlit**, **TextBlob**, **Pandas**, and **Matplotlib**.

## Live Demo

🔗 [Click here to try the app](https://your-deployed-app-url.streamlit.app)  
*(Replace with your actual deployed app link)*

## Features

- Upload reviews in bulk via CSV
- Predict sentiment for custom input
- Auto-generate missing titles and years
- Interactive charts:
  - Sentiment distribution (bar, pie)
  - Show-wise sentiment comparison

## Dataset Format

Your CSV should contain at least:
- `review` (text)
- `sentiment` (positive / negative)

Optional:
- `title` (auto-generated if missing)
- `year` (auto-generated if missing)

### Example

```csv
review,sentiment,title,year
"Amazing story",positive,Stranger Things,2019
"Too slow",negative,,
````

## Installation

Clone the repository and run locally:

```bash
git clone https://github.com/your-username/netflix-sentiment-analyzer.git
cd netflix-sentiment-analyzer
pip install -r requirements.txt
python -m textblob.download_corpora
streamlit run app.py
```

## Requirements

```
streamlit==1.35.0  
pandas==2.2.2  
textblob==0.17.1  
matplotlib==3.8.4  
nltk==3.8.1
```

## Deployment

To deploy on Streamlit Cloud:

1. Push your project to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your repo and set `app.py` as the entry point
4. Click “Deploy”

## License

This project is licensed under the MIT License.

```
