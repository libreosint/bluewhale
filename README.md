# Blue Whale
Bluesky public API wrapper

## Usage
```python
from bluewhale import BlueWhale

bw = BlueWhale()

# Get user profile
profile = bw.user_profile("forbes.com")
print(profile.displayName, profile.followersCount)

# Search users
results = bw.user_search("john")

# Get user feed
feed = bw.user_feed("forbes.com", limit=10)

# Get trending topics
topics = bw.trending_topics(limit=10)
```

## Examples

See [bluewhale.ipynb](bluewhale.ipynb) for interactive examples.

## License

MIT License
