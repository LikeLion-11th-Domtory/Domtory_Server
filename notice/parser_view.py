from .models import NoticeList
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

class CrawlDataView(APIView):
    def get(self, request, *args, **kwargs):
        # Set the starting page
        current_page = 0
        all_posts_data = []

        # Scrape all pages
        while True:
            posts_data = self.scrape_page(current_page)
            if not posts_data:
                break  # If no more data on the page, break the loop
            all_posts_data.extend(posts_data)
            current_page += 1
        # Reverse the order of the posts data list
        reversed_posts_data = reversed(all_posts_data)

        for post in reversed_posts_data:
            if not NoticeList.objects.filter(post_id=post['post_id']).exists():
                NoticeList(
                    post_id=post['post_id'],
                    title=post['title'],
                    date=post['date'],
                    content=post['content'],
                    images=post['images']).save()

        return Response(all_posts_data, status=status.HTTP_200_OK)

    def scrape_page(self, page):
        # Construct the URL for the specific page
        url = f"http://cbhs2.kr/0000007?where=&keyword=&page={page}"

        # Get the content of the page
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the links to the posts on the page
        posts = soup.select(".Board_LISTC .mr_TITLE a")

        # Create new links for each post on the page
        new_links = []
        for post in posts:
            link = post.attrs.get('onclick', '')
            post_id_start = link.find("goRead('") + len("goRead('")
            post_id_end = link.find("')", post_id_start)
            post_id = link[post_id_start:post_id_end]
            new_url = f"http://cbhs2.kr/0000007?postId={post_id}&mode=READ&where=&keyword=&page={page}"
            new_links.append(new_url)

        # List to store post data
        post_data_list = []

        # Iterate through each post link and scrape data
        for new_link in new_links:
            response = requests.get(new_link)
            soup = BeautifulSoup(response.text, 'html.parser')
            post_data = {}

            # Extract post_id
            post_id_element = soup.select_one('#postId')
            if post_id_element:
                post_data['post_id'] = post_id_element.get('value')

            # Extract title
            title_element = soup.select_one(".v_TITLE")
            if title_element:
                post_data['title'] = title_element.get_text(strip=True)

            # Extract date
            date = soup.select_one(".TrRoll td[colspan='2']")
            if date:
                post_data['date'] = date.select_one(".v_DBDATE").get_text(strip=True)

            # Extract content
            content = soup.select_one(".v_view_b4")
            if content:
                paragraphs = content.select('p')
                content_text = '\n'.join(paragraph.get_text(strip=True) for paragraph in paragraphs)
                post_data['content'] = content_text

                # Extract image
                img_tag = content.select_one("img")
                if img_tag:
                    img_src_relative = img_tag.get("src")
                    img_src_absolute = urljoin(new_link, img_src_relative)
                    post_data['images'] = img_src_absolute
                else:
                    post_data['images'] = ''
                

            # Append post_data to the list
            post_data_list.append(post_data)

        return post_data_list
