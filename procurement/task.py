from celery import shared_task
import feedparser
import uuid
from procurement.models import Commodity, CommodityNews
from datetime import date, timedelta, datetime
from urllib.parse import quote
import logging

logger = logging.getLogger(__name__)

SEARCH_TERMS = [
    'coffee commodity price fluctuation', 'coffee geopolitical tensions', 'coffee logistics delays',
    'coffee shipping costs', 'coffee freight rates', 'coffee natural disasters', 'coffee labor strikes',
    'coffee market shortage', 'coffee procurement fraud', 'coffee supplier risk', 'coffee_global_demand_shift',
    'coffee manufacturing slowdown', 'coffee_regulatory_changes'
]

@shared_task
def fetch_commodity_news_task():
    commodity, _ = Commodity.objects.get_or_create(
        name="Coffee",
        defaults={"type": "raw_material", "unit_of_measure": "USD/kg"}
    )
    time_range_days = 2
    time_range_start = date.today() - timedelta(days=time_range_days)
    time_range_end = date.today()
    fetch_date = datetime.now()

    for term in SEARCH_TERMS:
        try:
            rss_url = f"https://news.google.com/rss/search?q={quote(term)}%20when%3A{time_range_days}d&hl=en-US&gl=US&ceid=US:en"
            feed = feedparser.parse(rss_url)
            articles = []
            for index, entry in enumerate(feed.entries[:5], start=1):
                try:
                    article = {
                        'id': str(uuid.uuid4()),  # Generate a UUID for each article
                        'title': entry.get('title', 'N/A'),
                        'link': entry.get('link', 'N/A'),
                        'published': entry.get('published', 'N/A'),
                        'source': entry.get('source', {}).get('title', 'N/A'),
                        'description': entry.get('description', 'N/A')
                    }
                    articles.append(article)
                    field_name = term.replace(' ', '_')
                    news_instance, created = CommodityNews.objects.get_or_create(
                        commodity=commodity,
                        article_data=article,
                        defaults={
                            'fetch_date': {'date': fetch_date.strftime('%Y-%m-%d %H:%M:%S')},
                            'time_range_start': {'date': time_range_start.strftime('%Y-%m-%d')},
                            'time_range_end': {'date': time_range_end.strftime('%Y-%m-%d')},
                            field_name: [article]
                        }
                    )
                    if not created:
                        current_articles = getattr(news_instance, field_name, [])
                        if article['id'] not in [a['id'] for a in current_articles]:
                            current_articles.append(article)
                            setattr(news_instance, field_name, current_articles)
                            news_instance.save()
                except Exception as e:
                    logger.error(f"Error processing article for '{term}' (id: {article['id']}): {e}")
                    continue
            logger.info(f"Fetched {len(articles)} articles for '{term}'")
        except Exception as e:
            logger.error(f"Error fetching news for '{term}': {e}")
            continue