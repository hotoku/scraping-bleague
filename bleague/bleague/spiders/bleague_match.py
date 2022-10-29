import scrapy
from scrapy.http import HtmlResponse


from ..items import BleagueItem


def parse_query(url: str) -> dict[str, str]:
    if not "?" in url:
        return {}
    _, query = url.split("?")
    items = query.split("&")
    ret = {}
    for item in items:
        k, v = item.split("=")
        ret[k] = v
    return ret


def make_url(year: int | str, month: int | str, day: int | str | None = None) -> str:
    url = f"https://www.bleague.jp/schedule/?tab=1&year={year}&mon={month}&event=7&club="
    if day:
        url += f"&day={day}"
    return url


class BleagueMatchSpider(scrapy.Spider):
    name = "bleague-match"
    allowed_domains = ["www.bleague.jp"]
    start_urls = [
        make_url(2022, 11),
        make_url(2022, 12),
        make_url(2023, 1),
        make_url(2023, 2),
        make_url(2023, 3),
        make_url(2023, 4)
    ]

    def parse(self, response):
        if not isinstance(response, HtmlResponse):
            return

        days = set(response.xpath(
            '//div[contains(@class, "date-picker")]//span[contains(@class, "day")]/text()').getall())

        query = parse_query(response.url)
        year = query["year"]
        month = query["mon"]
        for day in days:
            yield response.follow(make_url(year, month, day), self.parse_match)

    def parse_match(self, response):
        if not isinstance(response, HtmlResponse):
            return

        xpath = """//ul[contains(@class, "round-list")]
                    /li[contains(@class, "list-item")]"""
        matches = response.xpath(xpath)
        homes = matches.xpath(
            '//span[contains(@class, "team home")]//text()').getall()
        aways = matches.xpath(
            '//span[contains(@class, "team away")]//text()').getall()
        arenas = response.xpath("""//span[parent::div[@class="info-arena"] and
                                          position()=2]/text()""").getall()
        start = response.xpath("""//span[parent::div[@class="info-arena"] and
                                          position()=3]/text()""").getall()

        query = parse_query(response.url)
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        for h, a, ar, s in zip(homes, aways, arenas, start):
            print("match data",
                  query["year"],
                  query["mon"],
                  query["day"],
                  s.strip(),
                  h.strip(),
                  a.strip(),
                  ar.strip(),
                  sep="\t")
            yield BleagueItem(
                year=query["year"],
                month=query["mon"],
                day=query["day"],
                start_time=s.strip(),
                home=h.strip(),
                away=a.strip(),
                arena=ar.strip()
            )
