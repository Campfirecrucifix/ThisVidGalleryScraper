import requests
import os
from bs4 import BeautifulSoup


def create_folder():
    # Check if the folder exists
    if not os.path.exists('Pics'):
        # Create the folder
        os.makedirs('Pics')


def get_num_pages(url):
    # Make a request to the website
    r = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find the pagination-last li tag
    last_page_li = soup.find('li', {'class': 'pagination-last'})

    # Find the 'a' tag within the li tag
    last_page_link = last_page_li.find('a')

    # Get the href attribute of the 'a' tag
    last_page_url = last_page_link['href']

    # Split the URL by '/' and get the third to last element
    num_pages = last_page_url.split('/')[-2]

    # Convert the num_pages string to an integer
    num_pages = int(num_pages)

    return num_pages


def get_gallery_links(current_page_url):
    # Make a request to the website
    r = requests.get(current_page_url)

    # Parse the HTML content
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find the div with the class thumbs-items thumbs-photo
    div = soup.find('div', {'class': 'thumbs-items thumbs-photo'})

    # Find all the 'a' tags within the div
    a_tags = div.find_all('a')

    # Create an empty list to store the href attributes
    hrefs = []

    # Iterate over the 'a' tags and get the href attribute
    for a in a_tags:
        href = a['href']
        hrefs.append(href)

    return hrefs


def get_picture_links(gallery_url):
    # Make a request to the website
    r = requests.get(gallery_url)

    # Parse the HTML content
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find the div with the class album-list
    div = soup.find('div', {'class': 'album-list'})

    # Find all the 'a' tags within the div
    a_tags = div.find_all('a')

    # Create an empty list to store the links
    links = []

    # Iterate over the 'a' tags and get the href attribute
    for a in a_tags:
        href = a['href']
        links.append(href)

    return links


def get_individual_picture_link(url):
    # Make a request to the website
    r = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find the div with the class photo-holder
    div = soup.find('div', {'class': 'photo-holder'})

    # Find the img tag within the div
    img = div.find('img')

    # Get the src attribute of the img tag
    picture_link = img['src']

    return picture_link


def get_folder_title_and_tags(url):
    # Make a request to the website
    r = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find the div with the class headline
    div = soup.find('div', {'class': 'headline'})

    # Find the h1 tag within the div
    h1 = div.find('h1')

    # Get the text of the h1 tag
    title = h1.text

    # Find the ul with the class description
    ul = soup.find('ul', {'class': 'description'})

    # Find the third li tag within the ul
    li = ul.find_all('li')[2]

    # Find all the 'a' tags within the li tag
    a_tags = li.find_all('a')

    # Create an empty list to store the tags
    tags = []

    # Iterate over the 'a' tags and get the text
    for a in a_tags:
        tag = a.text
        tags.append(tag)

    # Join the tags with a comma and a space
    tags_string = ', '.join(tags)

    return title, tags_string


def create_gallery_folder(title):
    # Create the path to the Pics folder
    pics_folder = 'Pics'

    # Check if the Pics folder exists
    if not os.path.exists(pics_folder):
        # If the Pics folder doesn't exist, create it
        os.makedirs(pics_folder)

    # Create the path to the new folder
    gallery_folder = os.path.join(pics_folder, title)

    # Check if the folder already exists
    if not os.path.exists(gallery_folder):
        # If the folder doesn't exist, create it
        os.makedirs(gallery_folder)

    # Return the path to the folder
    return gallery_folder


def save_pic_and_tags(direct_picture_link, path, tags):
    # Split the direct picture link to get the file name
    file_name = direct_picture_link.split('/')[-1]

    # Get the name of the picture without the extension
    picture_name = file_name.split('.')[0]

    # Create the path to the picture
    picture_path = os.path.join(path, file_name)

    # Create the path to the text file
    text_path = os.path.join(path, picture_name + '.txt')

    # Download the picture and save it to the path
    r = requests.get(direct_picture_link, allow_redirects=True)
    open(picture_path, 'wb').write(r.content)

    # Write the tags to the text file
    with open(text_path, 'w') as f:
        f.write(tags)


print('Please enter the thisvid url you would like to scrape. Ex: https://thisvid.com/albums/categories/anal/')
url = input('Enter the URL: ')
print('Scraping images from', url)
url = ''
num_pages = get_num_pages(url)
print("There are " + str(num_pages) + " pages to scrape.")
create_folder()

# Loop over the pages
for i in range(1, num_pages + 1):
    # Construct the URL for the current page
    current_page_url = url + str(i) + '/'

    # Get the gallery links for the current page
    galleries = get_gallery_links(current_page_url)

    # Loop over the galleries
    for gallery_url in galleries:
        # Get the picture links for the current gallery
        links = get_picture_links(gallery_url)
        title, tags = get_folder_title_and_tags(gallery_url)
        print('Now scraping: ' + title)
        path = create_gallery_folder(title)

        # Loop over the picture links
        for link in links:
            # Get the individual picture link
            direct_picture_link = get_individual_picture_link(link)
            save_pic_and_tags(direct_picture_link, path, tags)

print("Done scraping!")