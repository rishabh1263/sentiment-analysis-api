from  flask import Flask, jsonify, request
from textblob import TextBlob #> for text proceessing used in nlp . here we will use for sentiment analysis
import praw #>> python lib thatt allows to fetch data from redddit

## Initialize the flask app
app = Flask(__name__)

##Initialize the Reddit Api from praw
reddit = praw.Reddit(client_id= "F4VaZ_PKFHbJ1z5edQRYVA",
                    client_secret = "skpe2S4J2Ake4_b1PmwgqUOdfMW4Yw",
                    user_agent =  "sentiment_analysis v1.0 by RishabhSingh (rishabhajitsingh@shooliniuniversity.com)" )


## Function to analyse sentiment

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"
    
## Endpoint to analyze reddit post or comment sentiment

@app.route('/analyze', methods=['GET'])
def analyze():
    # Get the post ID from the query parameters
    post_id = request.args.get('post_id')
    
    # Check if the post_id is missing
    if not post_id:
        return jsonify({"error": "Missing 'post_id' parameter"}), 400

    try:
        # Fetch the Reddit post using the post_id
        post = reddit.submission(id=post_id)
        
        # Combine the title and content of the post for sentiment analysis
        full_text = post.title + " " + post.selftext
        
        # Analyze the sentiment of the full text
        sentiment = analyze_sentiment(full_text)
        
        # Return the sentiment result as JSON
        return jsonify({"sentiment": sentiment})
    
    except Exception as e:
        # Handle any errors (invalid post_id, Reddit API issues, etc.)
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)



