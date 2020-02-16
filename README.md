# get_podcasts.py
Downloads podcasts from RSS feeds one epsiode at a time.   
    
Uses details saved in CSV file, `podcast_details.csv`, which is updated each run with the next episode number to download.

Relies on save_rss_podcasts.py (below).

# save_rss_podcasts.py

Downloads podcast episodes from RSS feeds based on requested episode number(s).

Looks for episode number in the title, which might not be reliable in some circumstances.

## Requires
feedparser Python module

