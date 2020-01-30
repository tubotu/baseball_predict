
def make_soup(soup):
    """
    Get soup object from the specified url.
    """
    sleep_time = 3
    time.sleep(sleep_time)
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    return soup