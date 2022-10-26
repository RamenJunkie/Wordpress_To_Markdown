from bs4 import BeautifulSoup
from html import unescape
import os, os.path
import sys

file="test.xml"

try:
    file = sys.argv[1]
except:
    print("No file found")
    quit(__name__)

## I prefer formatting YYYY.MM.DD but if you want something besides a . replace it here
sep = "."
folder = "output_files"

def clean_text(post_text):
    ## Some HTML Tags and nonsense to strip out of every post.  More can be added
    replace_strings = ["<p>", "</p>", "<!-- wp:paragraph -->", "<!-- /wp:paragraph -->", "<!-- /wp:image -->",
                      '<!-- wp:image {"linkDestination":"custom"} -->', '">', "&nbsp;"]
    for each in replace_strings:
        post_text = post_text.replace(each, "")

    ### Make a vague attempt to convery links into Markdown Links
    post_text = post_text.replace('<a href="', "[")
    post_text = post_text.replace('</a>', "](Link)")

    ### I can't embed an image in a markdown file anyway, so when an image shows up, just remove it.
    while "<figure" in post_text:
        img_start = post_text.rfind("<figure")
        img_end = post_text.rfind("</figure>")+9
        post_text = post_text[0:img_start]+post_text[img_end:]

    while "< !--" in post_text:
        start = post_text.rfind("< !--")
        end = post_text.rfind("-->")+3
        post_text = post_text[0:start]+post_text[end:]

    ### There is a lot of white space going on, so we are going to strip that out.
    while "\n\n\n" in post_text:
        post_text = post_text.replace('\n\n\n', "\n\n")

    return post_text

with open(file, "r",encoding='utf-8') as file_read:
    posts = file_read.read()

soup = BeautifulSoup(posts, "xml")

#print(soup)
items = soup.findAll("item")
#print(len(items))

for each in items:
    post_content_dirty = unescape(str(each("content:encoded"))[18:-19])
    post_content = clean_text(post_content_dirty)

    ### We only care about posts, so we look for things with Post Content that aren't tags or images or whatever
    if len(post_content) > 3:
        ## characters not allowed in file names
        bad_chars = ["<",">",":",'"',"/","|","?","*"]
        title = str(each("title"))[8:-9].split(" [ID")[0]
        date_formatted = str(each("post_modified"))[19:-29].replace("-", sep)
        post_content = f"## {title}\n\n{post_content}"

        for char in bad_chars:
            title = title.replace(char, "")
        filename = f"{date_formatted} - {title}"

        try:
            with open("output_files/"+filename + '.md', 'w+') as output:
                output.write(post_content)
        except:
            pass
