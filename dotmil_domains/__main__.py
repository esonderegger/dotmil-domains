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


def sort_domains(domain_list):
    reversed_domains = []
    sorted_domains = []
    for x in domain_list:
        d = x.strip().split('.')
        d.reverse()
        reversed_domains.append(d)
    reversed_domains.sort()
    for y in reversed_domains:
        y.reverse()
        sorted_domains.append('.'.join(y))
    return sorted_domains


def domains_as_sorted_tuples():
    domains_dict = {}
    pages_to_scan = alphabet_pages()
    pages_to_scan += air_force_site_pages()
    for page in pages_to_scan:
        soup = soup_from_url(page)
        if soup:
            all_links = soup.find_all('a')
            for link in all_links:
                if ('href' in link.attrs) and link_is_http(link.attrs['href']):
                    absolute = urlparse.urljoin(page, link.attrs['href'])
                    domain = urlparse.urlsplit(absolute)[1]
                    if (domain.split('.')[0] == 'www'):
                        domain = '.'.join(domain.split('.')[1:])
                    if domain.endswith('.mil') and domain not in domains_dict:
                        if link.string:
                            domains_dict[domain] = link.string.strip()
                        else:
                            domains_dict[domain] = "Unknown"
                    elif (domain.endswith('.mil') and
                          domains_dict[domain] == "Unknown"):
                            if link.string:
                                domains_dict[domain] = link.string.strip()
        else:
            logging.warning('we will need to re-scan: ' + page)

    with open('mil.csv') as csvfile:
        milreader = csv.reader(csvfile)
        for row in milreader:
            if (row[0] not in domains_dict):
                domains_dict[row[0]] = "Unknown"

    list_to_sort = []
    for d in domains_dict:
        list_to_sort.append(d)
    sorted_list = sort_domains(list_to_sort)
    domain_tuples = []
    for d in sorted_list:
        domain_tuples.append((d, domains_dict[d]))
    return domain_tuples


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


def alphabet_pages():
    start_url = 'http://www.defense.gov/registeredsites/RegisteredSites.aspx'
    pages = []
    soup = soup_from_url(start_url)
    if soup:
        all_links = soup.find_all('a')
        for link in all_links:
            if (link.attrs['href'].startswith('RegisteredSites')):
                absolute = urlparse.urljoin(start_url,
                                            link.attrs['href'], True)
                pages.append(absolute)
    else:
        logging.warning('we will need to re-scan: ' + start_url)
    return pages


def air_force_site_pages():
    af_list = ['http://www.af.mil/AFSites.aspx']
    af_list.append('http://www.af.mil/AFSites.aspx?srBaseList=A')
    return af_list


def main():
    logging.basicConfig(level=logging.DEBUG)
    with open('dotmil-domains.csv', 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Domain Name', 'Organization'])
        domain_objects = domains_as_sorted_tuples()
        for d in domain_objects:
            csv_writer.writerow(d)


if __name__ == "__main__":
    main()
