# Reddit web scraping - Bella Ward

import requests
from bs4 import BeautifulSoup

# sorts to iterate through: controversial, gilded, hot, new, rising, top
import praw
import csv
import datetime
import time


# getting into Reddit API
# insert own client_id and client_secret from reddit account.
user_agent = "Scraper 1 by bella"
reddit = praw.Reddit(
    client_id="############", 
    client_secret="################",
    user_agent=user_agent
)

# for submission in reddit.subreddit("ChatGPT").hot(limit=1):
#     print(submission.title)
#     submission.comments.replace_more(limit=10)  # to get all comments in a submission
#     all_comments = submission.comments.list()
#     for comment in all_comments:
#         print(comment.body)


def get_top_replies(comment):
    replies = comment.replies
    sorted_replies = sorted(replies, key=lambda x: x.score, reverse=True)
    top_replies = [(reply.body, reply.created_utc) for reply in sorted_replies[:15]]
    return top_replies

# Get 35 posts from the "ChatGPT" subreddit - using [hot, top, controversial, gilded]
chatgpt_submissions = reddit.subreddit("ChatGPT").gilded(limit=35)

# Get 35 posts from the "GithubCopilot" subreddit - using [hot, top, controversial, gilded]
githubcopilot_submissions = reddit.subreddit("GithubCopilot").gilded(limit=35)

all_submissions = list(chatgpt_submissions) + list(githubcopilot_submissions)

csv_filename = "reddit_gilded_70_1.csv"

# Number of seconds to wait between requests:   
request_delay = 15  

with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Source", "URL", "Title", "Search term", "Question",
                     "Question Timestamp", "Question Votes", "Answer", "Answer Timestamp", "Answer Votes", "Sentiment analysis"])

    for submission in all_submissions:
        source = "Reddit"
        url = submission.url
        title = submission.title
        search_term = "ChatGPT" if "ChatGPT" in submission.subreddit.display_name else "GithubCopilot"
        question = submission.selftext
        question_timestamp = datetime.datetime.fromtimestamp(submission.created_utc).strftime("%Y-%m-%d %H:%M:%S")
        question_votes = 0 if submission.score >= 0 else 1
        answers = []

        # Get all comments 
        submission.comments.replace_more(limit=None)
        all_comments = submission.comments.list()

        # Sort comments based on score
        sorted_comments = sorted(all_comments, key=lambda x: x.score, reverse=True)

        # Get the top 10 replies for each post
        for comment in sorted_comments[:10]:
            top_replies = get_top_replies(comment)
            answers.extend(top_replies)

        # Write post data to CSV
        for answer, answer_timestamp in answers:
            answer_votes = 0 if submission.score >= 0 else 1
            writer.writerow([source, url, title, search_term, question,
                             question_timestamp, question_votes, answer, datetime.datetime.fromtimestamp(answer_timestamp).strftime("%Y-%m-%d %H:%M:%S"), answer_votes, ""])

        # DELAY between requests
        time.sleep(request_delay)

print("Data successfully written to the CSV file:", csv_filename)














