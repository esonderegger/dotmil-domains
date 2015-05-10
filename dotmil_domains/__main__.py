import requests
import bs4
import urlparse
import csv
import logging


def link_is_http(href):
    if href.startswith('mailto:'):
        return False
    elif href.startswith('javascript:'):
        return False
    elif href.startswith('#'):
        return False
    else:
        return True


def domains_from_url(url):
    domains_list = []
    with open('mil.csv') as csvfile:
        milreader = csv.reader(csvfile)
        for row in milreader:
            domains_list.append(row[0])
    pages_to_scan = alphabet_pages(url)
    for page in pages_to_scan:
        soup = soup_from_url(page)
        if soup:
            all_links = soup.find_all('a')
            for link in all_links:
                absolute = urlparse.urljoin(url, link.attrs['href'])
                domain = urlparse.urlsplit(absolute)[1]
                if (domain.endswith('.mil') and domain not in domains_list):
                    domains_list.append(domain)
        else:
            logging.warning('we will need to re-scan: ' + page)
    return domains_list


def soup_from_url(url):
    try:
        logging.info('requesting: ' + url)
        resp = requests.get(url)
    except:
        logging.error('there was a problem getting: ' + url)
        resp = False
    if resp:
        try:
            soup = bs4.BeautifulSoup(resp.text)
            return soup
        except:
            logging.error('there was a problem creating soup from: ' + url)
    return False


def alphabet_pages(url):
    pages = []
    soup = soup_from_url(url)
    if soup:
        all_links = soup.find_all('a')
        for link in all_links:
            if (link.attrs['href'].startswith('RegisteredSites')):
                absolute = urlparse.urljoin(url, link.attrs['href'], True)
                pages.append(absolute)
    else:
        logging.warning('we will need to re-scan: ' + url)
    return pages


def main():
    start_url = 'http://www.defense.gov/registeredsites/RegisteredSites.aspx'
    with open('dotmil-domains.csv', 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        for domain in domains_from_url(start_url):
            csv_writer.writerow([domain])


if __name__ == "__main__":
    main()
