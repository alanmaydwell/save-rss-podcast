import urllib
import feedparser


class SaveRssPodcasts:
    def __init__(self, url, filename_start="podcast", no_download=False):
        """
        Helps download podcasts from RSS feeds
        Args:
            url: rss feed url
            filename_start: (optional) start of filename for each saved podcast
            no_download (bool): if True download of file won't take place
        """
        self.url = url
        self.filename_start = filename_start
        self.feed = feedparser.parse(url)
        self.titles = []
        self.no_download = no_download

    def show_latest_episodes(self, count=5):
        """Print titles of the most recent episodes"""
        for entry in self.feed.entries[:count]:
            print(entry.get("title", ""))

    def find_wanted_episodes(self, wanted_episodes):
        """Find wanted episodes using episode number and return a dictionary
        with the associated feedburner entries.
        Might be a bit dodgy as there doesn't seem to be a uniform way
        of specifying episode number in an RSS feed entry
        (e.g. can be "#1" or "54" or "Ep.1" or "34:")

        Tries to match by looking for wanted episode number anywhere in the title
        text. May get confused if there is a number in the title that's not
        episode number related.

        Args:
            wanted_episodes: iterable containing episode numbers (can be int or str)

        Returns:
            dictionary with episode number (str) keys and feedburner entry
            values
        """
        wanted_episodes = [str(e) for e in wanted_episodes]
        found = {}
        for entry in self.feed.entries:
            title = entry.get("title", "")
            title_numbers = find_numbers_in_string(title)
            for title_number in title_numbers:
                if title_number in wanted_episodes:
                    found[title_number] = entry
        return found

    def save_episodes(self, wanted_episodes):
        """Save mp3 files associated with each wanted episode.
        Can cope with more than one file per episode.

        Filename generated from self.filename_start, then the episode title
        and, if there's more than one file in the episode, a sequence number too.

        Args:
            wanted_episodes: iterable containing episode numbers (can be int or str)
        Returns:
            list of successfully downloaded episodes
        """
        episodes = self.find_wanted_episodes(wanted_episodes)
        successful_downloads = []
        for episode, entry in episodes.items():
            # Construct middle part of filename from the podcast title
            title = entry.get("title", "no-title")
            filename_middle = "".join([c for c in title if c not in r""" :"'\/!"""])
            links = entry.get("links")
            audio_links = [l for l in links if l.get("type", "") == "audio/mpeg"]
            for ali, audio_link in enumerate(audio_links):
                url = audio_link.get("href", "")
                if url:
                    # Construct filename
                    filename = self.filename_start + filename_middle
                    if len(audio_links) > 1:
                        filename = filename + f"({ali})"
                    filename = filename + ".mp3"
                    # Download and save
                    # todo - (i)add exception handling (ii) download progress indicator
                    if not self.no_download:
                        urllib.request.urlretrieve(url, filename)
                        print("Saved:", filename)
                        successful_downloads.append(episode)
                    else:
                        print("Not downloaded:", filename)
        return successful_downloads


def find_numbers_in_string(text):
    """Find and return the parts of string containing numbers"""
    # Below seems more elegant but fails if number doesn't have a space
    # at either side, e.g. 11: or 3# or Ep.1
    ##extracted_numbers = [c for c in str.split() if c.isdigit()]
    extracted_numbers = []
    temp = ""
    for char in text:
        if char.isdigit():
            temp = temp + char
        else:
            if temp:
                extracted_numbers.append(temp)
                temp = ""
    return extracted_numbers


# Example use
if __name__ == "__main__":
    mince = SaveRssPodcasts("https://rss.acast.com/athleticomince", "mince-")
    mince.save_episodes([60, 61])
    rhlstp = SaveRssPodcasts("http://rss.acast.com/rhlstp", "")
    rhlstp.save_episodes([229])
