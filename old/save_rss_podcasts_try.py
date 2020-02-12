import urllib
import feedparser

def save_rss_podcasts(url, wanted_episodes, filename_start="", save=False):
    """
    Save podcasts from RSS feed
    Works by finding episode number in title text - might not be reliable
    Args:
        url - rss feed url
        wanted_episodes - episodes numbers to be downloaded (list of strings)
        file_name_start - optional start of filename for each saved podcast
        save - (bool) only actually downloads and saves when this is True
    """
    feed = feedparser.parse(url)
    for entry in feed.entries:
        title = entry.get("title", "")
        title_words = title.split(" ")

        # See if episode number extracted from title matches requested episode
        # Depends on episode number being 2nd item in title
        if title_words[1] in wanted_episodes:

            # Find the links within and extract those concerning audio files
            links = entry.get("links", "")
            audio_links = [l for l in links if l.get("type", "") == "audio/mpeg"]
            # Save each audio file found
            for ali, audio_link in enumerate(audio_links):
                url = audio_link.get("href", "")
                if url:
                    # Make filename from title but with some character sanitisation
                    filename = filename_start + "".join([c for c in title if c not in r""" :"'\/!"""])
                    # Extend filename if single episode has multiple files
                    if len(audio_links) > 1:
                        filename = filename + f"({ali})"
                    filename = filename + ".mp3"

                    if save:
                        print(f"Saving '{title}'' to {filename}")
                        urllib.request.urlretrieve(url, filename)
                    else:
                        print(f"Not saving '{title}'' to {filename}")
                else:
                    print("No mp3 files found for episode:", title)


url = "https://rss.acast.com/athleticomince"
filename_start = "Mince-"
wanted_episodes = ["54", "55"]
filename_start = "Mince-"

save_rss_podcasts(url, wanted_episodes, filename_start)