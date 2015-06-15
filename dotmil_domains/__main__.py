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


def dotmil_domains_dict(pages_to_scan):
    domains_dict = {}
    with open('mil.csv') as csvfile:
        milreader = csv.reader(csvfile)
        for row in milreader:
            domains_dict[row[0]] = row[1]
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
    return domains_dict


def domains_as_sorted_tuples():
    domains_dict = dotmil_domains_dict(mil_site_pages())
    domains_dict = add_comodo_domains(domains_dict)
    list_to_sort = []
    for d in domains_dict:
        list_to_sort.append(d)
    sorted_list = sort_domains(list_to_sort)
    domain_tuples = []
    for d in sorted_list:
        encoded_utf8 = domains_dict[d].encode('utf-8')
        white_space_reduced = " ".join(encoded_utf8.split())
        domain_tuples.append((d, white_space_reduced))
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


def mil_site_pages():
    sites = dod_site_pages()
    sites += air_force_site_pages()
    sites += army_site_pages()
    sites += navy_site_pages()
    sites += marine_site_pages()
    sites += uscg_site_pages()
    sites += national_guard_site_pages()
    return sites


def dod_site_pages():
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
    pages.append('http://dtic.mil/dtic/faqs/dtic_a_to_z.html')
    return pages


def air_force_site_pages():
    af_list = ['http://www.af.mil/AFSites.aspx']
    af_list.append('http://www.af.mil/AFSites.aspx?srBaseList=A')
    return af_list


def army_site_pages():
    return ['http://www.army.mil/info/a-z/']


def navy_site_pages():
    navy_list = ['http://www.navy.mil/navydata/infoIndex.asp']
    navy_list.append('http://www.navy.mil/links/alpha.asp')
    return navy_list


def marine_site_pages():
    marine_list = []
    for i in range(1, 7):
        page_link = "http://www.marines.mil/Units.aspx?srpage=" + str(i)
        marine_list.append(page_link)
    return marine_list


def uscg_site_pages():
    uscg_list = ['http://coastguard.dodlive.mil/official-sites']
    uscg_list.append('http://www.uscg.mil/lantarea/Links.asp')
    return uscg_list


def national_guard_site_pages():
    return ['http://www.nationalguard.mil/Resources/StateWebsites.aspx']


def add_comodo_domains(domains_dict):
    possible_domains = []
    edited_domains = []
    soup = soup_from_url('https://crt.sh/?dNSName=%25.mil')
    all_tds = soup.find_all('td')
    for td in all_tds:
        if td.string:
            td_text = td.string.strip().lower()
            if '.mil' in td_text:
                if ',' in td_text:
                    comma_split = td_text.split(',')
                    for d in comma_split:
                        possible_domains.append(d.strip())
                elif ' ' in td_text:
                    space_split = td_text.split(' ')
                    for d in space_split:
                        possible_domains.append(d.strip())
                else:
                    possible_domains.append(td_text)
    for possibility in possible_domains:
        if possibility.endswith('.mil'):
            if possibility.startswith('https://'):
                edited_domains.append(possibility[8:])
            elif possibility.startswith('www.'):
                edited_domains.append(possibility[4:])
            elif possibility.startswith('*'):
                dot_split = possibility.split('.')
                rebuilt = '.'.join(dot_split[1:])
                edited_domains.append(rebuilt)
            else:
                edited_domains.append(possibility)
    for domain in edited_domains:
        if domain not in domains_dict:
            domains_dict[domain] = "Unknown"
    return domains_dict


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
