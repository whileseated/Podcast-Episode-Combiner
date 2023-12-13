import requests
import xml.etree.ElementTree as ET
import subprocess
import os

def fetch_and_parse_rss(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return ET.fromstring(response.content)
    except requests.RequestException as e:
        print(f"Error fetching RSS feed: {e}")
        return None

def clean_url(url):
    return url.split('?', 1)[0]

def is_mp3_url(url):
    if '?' in url:
        url = url.split('?', 1)[0]
    return url.endswith('.mp3')

def find_mp3_links_and_durations(root):
    if root is None:
        return []
    
    mp3_data = []

    for item in root.findall('./channel/item'):
        enclosure = item.find('enclosure')
        itunes_duration = item.find('itunes:duration', namespaces={'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'})

        if enclosure is not None and 'url' in enclosure.attrib:
            url = enclosure.attrib['url']
            if is_mp3_url(url):
                duration_in_minutes = None
                if itunes_duration is not None and itunes_duration.text.isdigit():
                    duration_in_minutes = int(itunes_duration.text) // 60
                mp3_data.append((url, duration_in_minutes))

    return mp3_data


def download_and_combine_episodes(episodes, start, end, output_filename):
    temp_files = []
    for i in range(start, min(end, len(episodes))):
        url, _ = episodes[i]
        filename = f"temp_{i}.mp3"
        temp_files.append(filename)

        print(f"Downloading episode {i + 1}/{end}: ", end="")
        os.system(f"curl -s -L '{url}' -o {filename}")
        print("Done")

    print("Combining episodes...")
    with open('file_list.txt', 'w') as f:
        for file in temp_files:
            f.write(f"file '{file}'\n")

    # subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "file_list.txt", "-c", "copy", output_filename])
    subprocess.run(["ffmpeg", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "file_list.txt", "-c", "copy", output_filename])


    # Clean up temp files
    for file in temp_files:
        os.remove(file)
    os.remove('file_list.txt')
    print(f"Combined episodes saved as {output_filename}.")
def main():
    rss_url = input("RSS URL: ")
    root = fetch_and_parse_rss(rss_url)

    mp3_data = find_mp3_links_and_durations(root)
    mp3_data.reverse()

    print(f"{len(mp3_data)} episodes have been found.")
    for index, (url, duration) in enumerate(mp3_data, start=1):
        duration_str = f"{duration} minutes" if duration is not None else "Unknown duration"
        print(f"{index}. {url}, Duration: {duration_str}")

    # Ask user to combine episodes
    def ask_and_combine(subset_description, start, end):
        answer = input(f"Would you like to combine {subset_description}? (Y/N) ").strip().lower()
        if answer == 'y':
            download_and_combine_episodes(mp3_data, start, end, f"combined_{subset_description.replace(' ', '_')}.mp3")
            return True
        return False

    num_episodes = len(mp3_data)
    if num_episodes > 0:
        if ask_and_combine("all episodes", 0, num_episodes):
            return

        if num_episodes >= 5 and ask_and_combine("the last five episodes", num_episodes - 5, num_episodes):
            return

        if num_episodes >= 3 and ask_and_combine("the last three episodes", num_episodes - 3, num_episodes):
            return

        print("OK, check back with me when I can assist you.")

if __name__ == "__main__":
    main()

