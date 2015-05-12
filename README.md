# dotmil-domains
An incomplete listing of `.mil` domains and the code for the scraper used to build the list

## Why?

There currently isn't a publicly available directory of all the domain names registered under the US military's `.mil` top-level domain. Such a directory would be useful for people looking to get an aggregate view of military websites and how they are hosted. For example, [Ben Balter](http://ben.balter.com) has been doing some great work [analyzing](http://ben.balter.com/2015/05/11/third-analysis-of-federal-executive-dotgovs/) the [official set of .gov domains](https://github.com/GSA/data/tree/gh-pages/dotgov-domains).

This is by no means an official or a complete list. It is intended to be a first step toward a better understanding of how the military is managing its domain name space and official sites.

You can download this list [as a .csv file](https://raw.githubusercontent.com/esonderegger/dotmil-domains/master/dotmil-domains.csv) or view it with [github's pretty formatting](https://github.com/esonderegger/dotmil-domains/blob/master/dotmil-domains.csv).

## How?

This list is populated by a scraper script, written in python, that crawls some official site listing pages.

To run the script yourself, open a terminal and type:

    git clone https://github.com/esonderegger/dotmil-domains.git
    cd dotmil-domains

I strongly suggest using [virtualenv](https://virtualenv.pypa.io/en/latest/) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) for managing python environments. The installation instructions for those tools are done better than I could ever write on their respective pages. Once you have created and activated your virtualenv, type:

    python setup.py develop
    dotmil-domains

This will install the two dependencies ([Requests](http://docs.python-requests.org/en/latest/) and [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/)) into your virtualenv, link the `dotmil-domains` command to the `__main__.py` script in the `dotmil_domains` directory, and then run the command to create a new `dotmil-domains.csv` file. The `develop` after the `python setup.py` means that you can make changes to the `__main__.py` script, run `dotmil-domains` again and see the new file.

## Contributing

I'd love to have some help with this! Please feel free to [create an issue](https://github.com/esonderegger/dotmil-domains/issues) or [submit a pull request](https://github.com/esonderegger/dotmil-domains/pulls) if you notice something that can be better. Specifically, suggesting additional pages we can scrape and domains that are either not found or have incorrect organization names associated with them would be very helpful.

## todo:

- Manually add the remaining "Unknown" domains to the `mil.csv` file
- Find some more pages to scrape
- Write some comments explaining how the python code is structured
- Add some columns to the csv with whether or not the domain is still active, redirects somewhere else, etc.?
