# reddit_scraper

Python toolkit for collecting and analyzing Reddit user data. Two approaches: a **PullPush API client** for live queries and a **Pushshift `.zst` dump parser** with multiprocessing for offline bulk analysis.

![Python](https://img.shields.io/badge/Python-3-blue) ![Pushshift](https://img.shields.io/badge/Data-Pushshift-orange) ![PullPush](https://img.shields.io/badge/API-PullPush.io-green)

---

## How It Works

```
┌────────────────────────────────┐     ┌────────────────────────────────────┐
│    PullPush API (pullpush/)    │     │   Pushshift Dumps (pushshift_data/)│
│                                │     │                                    │
│  Subreddit ──▶ Gather Users    │     │  .zst file ──▶ Stream Decompress   │
│  User ──▶ Full Post History    │     │  ──▶ Parse JSON Lines              │
│  ──▶ Cross-Sub Analysis        │     │  ──▶ Filter by Subreddit/User      │
│  ──▶ Export JSON               │     │  ──▶ Export User Data              │
└────────────────────────────────┘     └────────────────────────────────────┘
```

**PullPush** — query the API for real-time data. Good for targeted scraping of specific users or subreddits.

**Pushshift Dumps** — process archived Reddit data dumps (`.zst` compressed). Good for bulk analysis across months/years of data. Supports single-threaded and multiprocessing modes.

---

## Project Structure

```
reddit_scraper/
├── pullpush/                         # PullPush API client
│   ├── redditscraper.py              # API wrapper — query builder + JSON parser
│   ├── gather_users.py               # Collect unique users from a subreddit
│   ├── user_stalker.py               # Scrape a user's full post/comment history
│   ├── user_sub_stalker.py           # Pipeline: gather users → scrape all their data
│   └── utils.py                      # Progress bar utility
│
├── pushshift_data/                   # Pushshift .zst dump processor
│   ├── single/                       # Single-threaded processing
│   │   ├── single_process.py         # Stream decompress .zst, parse, filter, extract
│   │   ├── parser.py                 # JSON line parser (comments + submissions)
│   │   ├── user.py                   # User set with file persistence
│   │   └── user_data.py              # User→posts mapping with JSON export
│   ├── multi/                        # Multiprocessing
│   │   ├── multi_process_zst.py      # Split .zst across CPU cores for parallel decompression
│   │   └── sequential_multi_process_zst.py  # Sequential variant with benchmarking
│   └── tests/                        # Multiprocessing experiments
│       ├── parallel.py
│       ├── workers.py
│       └── zst_part_process.py
│
├── requirements.txt                  # requests, zstandard
└── setup.sh                          # Venv setup + dependency install
```

---

## PullPush API Client

Query the [PullPush.io](https://pullpush.io/) API (Pushshift successor) for live Reddit data.

### Classes

| Class | Purpose |
|-------|---------|
| `redditScraper` | Query builder — set subreddit, author, time range, size |
| `redditParser` | Response parser — extract users, timestamps, subreddits, text |

### Scripts

| Script | What it does |
|--------|-------------|
| `gather_users.py` | Collects unique usernames from a subreddit by paginating through submissions or comments |
| `user_stalker.py` | Scrapes a single user's entire post and comment history across all subreddits |
| `user_sub_stalker.py` | Full pipeline — gathers users from a sub, then scrapes all their data. Exports to JSON |

### Example

```python
from redditscraper import redditScraper, redditParser

scraper = redditScraper('submission')
scraper.setSub('AskReddit')
scraper.setSize(100)

data = scraper.scrape()
parser = redditParser(data)

print(parser.getUsers())    # list of usernames
print(parser.getTimes())    # human-readable timestamps
print(parser.getText())     # post titles + bodies
```

---

## Pushshift Data Dumps

Process raw Pushshift archive files (`.zst` Zstandard compressed NDJSON). These are multi-GB dumps of all Reddit comments/submissions by month.

### Features

- **Stream decompression** — processes data in chunks without loading the full file into memory
- **Resumable** — saves file seek position on keyboard interrupt or errors, resumes from where it left off
- **Multiprocessing** — splits the compressed file across CPU cores for parallel decompression
- **Subreddit filtering** — extract users and posts from target subreddits
- **Comment + submission parsing** — handles both `body` (comments) and `title`/`selftext` (submissions)

### Usage

```bash
# Single-threaded: process one or more .zst files
cd pushshift_data/single
python single_process.py RC_2024-01.zst RC_2024-02.zst

# Multi-process: parallel decompression
cd pushshift_data/multi
python multi_process_zst.py RC_2024-01.zst
```

If interrupted, a `.save` file is created with the byte offset. Re-running automatically resumes from that point.

---

## Getting Started

```bash
# Set up virtual environment and install dependencies
./setup.sh

# Or manually
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Dependencies

- `requests` — HTTP client for PullPush API
- `zstandard` — Zstandard decompression for Pushshift dumps
