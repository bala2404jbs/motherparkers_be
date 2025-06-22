# # Service for fetching commodity data from external APIs
# import requests

# def fetch_commodity_prices(api_url, params=None, headers=None):
#     response = requests.get(api_url, params=params, headers=headers)
#     response.raise_for_status()
#     return response.json()

import feedparser
from django.core.management.base import BaseCommand
from procurement.models import Commodity, CommodityNews
from datetime import date, timedelta
from urllib.parse import quote
import logging

logger = logging.getLogger(__name__)

# Search terms related to coffee
SEARCH_TERMS = [
    'coffee commodity price fluctuation', 'coffee geopolitical tensions', 'coffee logistics delays',
    'coffee shipping costs', 'coffee freight rates', 'coffee natural disasters', 'coffee labor strikes',
    'coffee market shortage','coffee procurement fraud', 'coffee supplier risk', 'coffee global demand shift',
    'coffee manufacturing slowdown','coffee regulatory changes'
]


class Command(BaseCommand):
    help = "Fetch and save coffee-related news from Google News RSS"

    def fetch_google_news(self, query: str, max_entries: int = 5, time_range_days: int = 1):
        try:
            # Construct RSS URL with time range (e.g., when:10d)
            rss_url = f"https://news.google.com/rss/search?q={quote(query)}%20when%3A{time_range_days}d&hl=en-US&gl=US&ceid=US:en"
            feed = feedparser.parse(rss_url)
            articles = []
            for entry in feed.entries[:max_entries]:
                try:
                    article = {
                        'title': entry.get('title', 'N/A'),
                        'link': entry.get('link', 'N/A'),
                        'published': entry.get('published', 'N/A'),
                        'source': entry.get('source', {}).get('title', 'N/A'),
                        'description': entry.get('description', 'N/A')
                    }
                    articles.append(article)
                except Exception as e:
                    logger.error(f"Error processing article for query '{query}': {e}")
                    continue  # Skip to next article
            return articles
        except Exception as e:
            logger.error(f"Error fetching news for query '{query}': {e}")
            return []  # Skip to next search term

    def handle(self, *args, **options):
        # Ensure Coffee commodity exists
        commodity, _ = Commodity.objects.get_or_create(
            name="Coffee",
            defaults={"type": "raw_material", "unit_of_measure": "USD/kg"}
        )

        # Time range based on when:10d
        time_range_days = 10
        time_range_start = date.today() - timedelta(days=time_range_days)
        time_range_end = date.today()

        for term in SEARCH_TERMS:
            articles = self.fetch_google_news(query=term, max_entries=5, time_range_days=time_range_days)
            if articles:
                self.stdout.write(f"Fetched {len(articles)} articles for '{term}'")
                for article in articles:
                    try:
                        CommodityNews.objects.get_or_create(
                            commodity=commodity,
                            search_term=term,
                            title=article['title'],
                            link=article['link'],
                            published=article['published'],
                            source=article['source'],
                            description=article['description'],
                            defaults={
                                'article_data': article,
                                'time_range_start': time_range_start,
                                'time_range_end': time_range_end
                            }
                        )
                    except Exception as e:
                        logger.error(f"Error saving article for '{term}' (title: {article['title']}): {e}")
                        continue  # Skip to next article
            else:
                self.stdout.write(self.style.WARNING(f"No articles found for '{term}'"))

        self.stdout.write(self.style.SUCCESS("Successfully fetched and saved commodity news"))