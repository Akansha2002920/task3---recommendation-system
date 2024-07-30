from flask import Flask, request, jsonify, render_template
import pandas as pd
from recommendation import get_recommendations

app = Flask(__name__)

# Load your data
try:
    user_item_matrix = pd.read_csv('data/user_item_matrix.csv', index_col=0)
    user_similarity_df = pd.read_csv('data/user_similarity_df.csv', index_col=0)
except FileNotFoundError as e:
    print(f"FileNotFoundError: {e}")
    raise

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    user_id = request.args.get('user_id')
    print(f"Received user_id: {user_id}")  # Debug print

    if not user_id:
        return jsonify({'error': 'User ID parameter is missing'}), 400

    if user_id not in user_similarity_df.index:
        return jsonify({'error': f"User ID {user_id} not found in user_similarity_df"}), 400

    try:
        recommendations = get_recommendations(user_id, user_item_matrix, user_similarity_df)
        return render_template('recommend.html', user_id=user_id, recommendations=recommendations.to_dict())
    except ValueError as e:
        print(f"ValueError: {e}")  # Debug print
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Exception: {e}")  # Debug print
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
