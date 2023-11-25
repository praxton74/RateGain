from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

def extract_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    article_names = []
    img_urls = []
    dates = []
    likes = []

    articles = soup.find_all('article', class_='blog-item')
    for article in articles:
        article_name = article.find('h6').find('a').text.strip()
        article_names.append(article_name)

        img_url = article.find('div', class_='img').find('a')['data-bg']
        img_urls.append(img_url)

        date = article.find('div', class_='bd-item').find('span').text.strip()
        dates.append(date)

        like_count = article.find('a', class_='zilla-likes').find('span').text.strip()
        likes.append(like_count)

    data = {
        'Article Name': article_names,
        'Image URL': img_urls,
        'Date': dates,
        'Likes': likes
    }
    df = pd.DataFrame(data)
    return df

@app.route('/', methods=['GET', 'POST'])
def process_html():
    if request.method == 'POST':
        html_content = request.form['html_content']
        df = extract_data(html_content)

        # Save DataFrame to Excel
        excel_path = 'output.xlsx'
        df.to_excel(excel_path, index=False)

        # Return the path to the saved Excel file
        return jsonify({'message': 'Data extracted and saved to ' + excel_path})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
