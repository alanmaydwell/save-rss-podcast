"""
Podcast episode saver.
Reads details from CSV file in particular format.
Automatically downloads next available episode on each run.
Updates CSV file afterwards with next episode to read.
Each run should result in next episode being saved, if one available.
"""

from save_rss_podcasts import SaveRssPodcasts

class PodCSVRead:
    """Read podcast RSS details from CSV file
    Stores extracted details in self.items
    Can also re-write the file with values from self.items.
    """
    def __init__(self, filename):
        """Read details from CSV file
        Args:
            filenam: filename of the CSV file
        """
        self.filename = filename
        self.items = []
        self.dict_keys = []
        self.readfile()

    def readfile(self):
        """Read and process each line from the CSV file"""
        with open(self.filename, "r") as infile:
            for line in infile:
                self.process_line(line)

    def process_line(self, line):
        """Process a line from the csv file and add details to self.items"""
        # skip "comment" lines starting with #
        if line.startswith("#"):
            return
        # Extract elements from line, also ensure str and remove lead/trail whitespace
        line_elements = [str(e).strip() for e in line.split(",")]
        # Headings
        if not self.dict_keys:
            self.dict_keys = line_elements
        # Data
        else:
            temp = {key: value for key, value in zip(self.dict_keys, line_elements)}
            self.items.append(temp)

    def save_file(self):
        """Save the CSV file with details from self.items"""
        with open(self.filename, "w") as outfile:
            # Heading row
            outfile.write(",".join(self.dict_keys) + "\n")
            # Data rows
            for item in self.items:
                elements = [item.get(key, "") for key in self.dict_keys]
                outfile.write(",".join(elements) + "\n")


if __name__ == "__main__":
    my_run = PodCSVRead("podcast_details.csv")
    # holds details of the episode numbers to to downloaded *after* this run
    # used to set the next episode number when updated CSV files saved at the end
    for my_item in my_run.items:
        url = my_item.get("url", "")
        filename_start = my_item.get("filename_start", "")
        episode_no = my_item.get("episode_no", "")
        print(url, filename_start, episode_no)
        podget = SaveRssPodcasts(url, filename_start)
        successful = podget.save_episodes([episode_no])
        # If download was successful, advance episode number by one for next time
        if episode_no in successful:
            my_item["episode_no"] = str(int(episode_no) + 1)

    # Re-write CSV file to capture any episode number increaments
    my_run.save_file()
