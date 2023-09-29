from base.scraping import BaseScraper


class WeblancerScraper(BaseScraper):

    base_url: str = 'https://weblancer.net'
    category_route: str = '/freelance'
