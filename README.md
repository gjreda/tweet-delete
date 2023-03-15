# tweet-delete

command-line utility for deleting my history of tweets.

### usage
This will delete all tweets that are more than 21 days old.
```python
$ python main.py --num_days_ago 21
```

### issues
Handling rate limits is overkill since this script can just run every few hours
