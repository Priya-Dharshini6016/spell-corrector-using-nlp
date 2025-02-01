from flask import Flask, request, jsonify
import nltk
from nltk.corpus import words
from difflib import get_close_matches

# Download the word list if not already downloaded
nltk.download('words')
word_list = set(words.words())

app = Flask(__name__)

def correct_spelling(word):
    """
    Return the closest matching word from the dictionary.
    If no match is found, return the original word.
    """
    matches = get_close_matches(word, word_list, n=1, cutoff=0.8)
    return matches[0] if matches else word

@app.route('/spell-check', methods=['POST'])
def spell_check():
    """
    API endpoint to process and correct spelling mistakes in text.
    """
    try:
        # Get input data from the request
        data = request.json
        text = data.get("text", "")

        # Correct spelling for each word
        corrected_text = " ".join([correct_spelling(word) for word in text.split()])

        # Return the corrected text
        return jsonify({"corrected_text": corrected_text}), 200

    except Exception as e:
        # Handle any errors
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
