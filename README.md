# Podcast Episode Combiner

This Python script is designed to download and combine podcast episodes from a specified RSS feed into a single MP3 file. It's suitable for users who are familiar with running Python scripts.

## Prerequisites

- Python installed on your system.
- `ffmpeg` must be installed and accessible in your system's PATH. This is crucial for the script to combine audio files.
- `curl` should be installed on your system as it is used for downloading episodes.

## Quick Start

1. **Clone the Repository or Download the Script**: Get the script onto your local machine.
2. **Install Required Python Packages**: Ensure `requests` is installed. You can install it using `pip`:

   ```pip install requests```
3. **Find Your Podcast's RSS Feed**: Visit [listennotes.com](https://www.listennotes.com), search for your podcast and copy the url of the RSS feed.

4. **Run the Script**: 

```python3 episode_combiner.py```

5. **Follow On-screen Prompts**: The script will ask for the RSS URL and other inputs as needed.

6. **Output**: The final combined MP3 file will be saved in the same directory as the script. Some podcast apps, like Pocketcast, allow you the ability to upload the mp3 as a new file, and the app will remember your progress through the file, just like an audiobook (or podcast).

## Notes

Why? In creating [DefunktCast](https://defunkt-cast.herokuapp.com/), I wondered why there are so few workable solutions for listening to older broadcasts. Podcasts are great while they're being published, but they require a lot of manual manipulation once the show is complete. This script is one solution for surfacing older (or dead!) podcasts.

This script is intended for combining podcast episodes. It may not work as expected with non-podcast RSS feeds, with podcasts exclusive to Spotify, or with files that are not in MP3 format.