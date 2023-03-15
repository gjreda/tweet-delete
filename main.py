from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import tweepy


load_dotenv()


class TweetDeleter:
    def __init__(self):
        self.auth = tweepy.OAuth2BearerHandler(bearer_token=os.environ.get('bearer_token'))
        self.client = tweepy.Client(
            consumer_key=os.environ.get('consumer_key'),
            consumer_secret=os.environ.get('consumer_secret'),
            access_token=os.environ.get('access_token'),
            access_token_secret=os.environ.get('access_token_secret'),
            bearer_token=os.environ.get('bearer_token')
        )
        self.me = self.client.get_me().data

    def get_tweets(self, **kwargs) -> tweepy.Response:
        return self.client.get_users_tweets(id=self.me.id, **kwargs)

    def delete_tweets(self, end_time) -> None:
        response = self.get_tweets(end_time=end_time)

        for tweet in response.data:
            print(f"deleting tweet {tweet.id}: {tweet.text[:40]} ...")
            self.client.delete_tweet(id=tweet.id)

        while response.meta.get('next_token'):
            response = self.get_tweets(pagination_token=response.meta['next_token'])

            for tweet in response.data:
                print(f"deleting tweet {tweet.id}: {tweet.text[:40]} ...")
                self.client.delete_tweet(id=tweet.id)


def main(num_days_ago: int) -> None:
    end_time = (datetime.utcnow() - timedelta(days=num_days_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")

    deleter = TweetDeleter()
    deleter.delete_tweets(end_time=end_time)


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--num_days_ago', type=int, required=True)
    args = parser.parse_args()

    main(num_days_ago=int(args.num_days_ago))
