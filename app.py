from flask import Flask, render_template, request
import pickle
import numpy as np
import gzip

# Load required data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
with gzip.open('books.pkl.gz', 'rb') as f:
    books = pickle.load(f)
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

# Default route now points to the recommendation page
@app.route('/')
def recommend_ui():
    return render_template('recommend.html', book_titles=list(pt.index))

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')

    # Check if user_input exists in pt.index
    if user_input not in pt.index:
        return render_template('recommend.html', data=[], error="Book not found. Please try a different title.", book_titles=list(pt.index), selected_book=user_input)

    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return render_template('recommend.html', data=data, book_titles=list(pt.index), selected_book=user_input)

if __name__ == '__main__':
    app.run(debug=True)
