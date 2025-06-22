# from rest_framework import viewsets, permissions
# from .models import *
# from .serializers import *

# class CommodityViewSet(viewsets.ModelViewSet):
#     queryset = Commodity.objects.all()
#     serializer_class = CommoditySerializer
#     permission_classes = [permissions.IsAuthenticated]

# class CommodityPriceViewSet(viewsets.ModelViewSet):
#     queryset = CommodityPrice.objects.all()
#     serializer_class = CommodityPriceSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class PricePredictionViewSet(viewsets.ModelViewSet):
#     queryset = PricePrediction.objects.all()
#     serializer_class = PricePredictionSerializer
#     permission_classes = [permissions.IsAuthenticated]

# # Add more ViewSets for other models as needed (RiskEvent, Supplier, PurchaseOrder, etc.)

from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Commodity, CommodityPrice, PricePrediction
from .serializers import CommoditySerializer, CommodityPriceSerializer, PricePredictionSerializer
from core.views import IsProcurementManager, IsAnalyticsUser

class CommodityViewSet(viewsets.ModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'type']
    search_fields = ['name', 'type']
    ordering_fields = ['name', 'type']

class CommodityPriceViewSet(viewsets.ModelViewSet):
    queryset = CommodityPrice.objects.all()
    serializer_class = CommodityPriceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['commodity', 'date', 'currency']
    search_fields = ['source_api']
    ordering_fields = ['date', 'price']

class PricePredictionViewSet(viewsets.ModelViewSet):
    queryset = PricePrediction.objects.all()
    serializer_class = PricePredictionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAnalyticsUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['commodity', 'prediction_date']
    ordering_fields = ['prediction_date', 'predicted_price', 'confidence_score']
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.db.models.expressions import RawSQL
from procurement.models import CommodityNews
from datetime import datetime
import openai
import os
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.db.models.expressions import RawSQL
from procurement.models import CommodityNews
from datetime import datetime, timedelta
import openai
import os
import json

# Configure OpenAI
openai.api_key = os.environ.get('OPENAI_API_KEY')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.db.models.expressions import RawSQL
from procurement.models import CommodityNews, ProcurementNewsSummary
from datetime import datetime, timedelta
import openai
import os
import json

# Configure OpenAI
openai.api_key = os.environ.get('OPENAI_API_KEY')

class ProcurementNewsAnalysisView(APIView):
    def get(self, request):
        # Filter by fetch_date matching the last 5 days
        current_date = datetime.now().date()
        start_date = current_date - timedelta(days=4)
        print(f"Date range for filtering: {start_date} to {current_date}")
        news_items = CommodityNews.objects.filter(
            fetch_date__isnull=False
        ).extra(
            where=["CAST((fetch_date->>'date') AS timestamp)::date BETWEEN %s AND %s"],
            params=[start_date, current_date]
        )
        print(f"Filtering news items for date range: {start_date} to {current_date}")
        print(f"Found {news_items.count()} news items in the date range.")

        if not news_items.exists():
            return Response({
                "summaries": [],
                "data": [],
                "note": "No articles found for the date range."
            }, status=status.HTTP_200_OK)

        # Extract relevant data from article_data
        articles = []
        for item in news_items:
            article_data = item.article_data
            articles.append({
                'id': article_data.get('id'),
                'title': article_data.get('title', 'N/A'),
                'source': article_data.get('source', 'N/A'),
                'published': article_data.get('published', 'N/A'),
                'uuid': item.id
            })

        if not articles:
            return Response({
                "summaries": [],
                "data": [],
                "note": "No valid article data found for the date range."
            }, status=status.HTTP_200_OK)

        # Optimized prompt for strict JSON output
        prompt = f"""
        Task: Analyze articles on coffee procurement issues (e.g., supply chain disruptions, price fluctuations).
        Steps: Prioritize up to 5 relevant articles based on supply chain impact, procurement relevance, and source credibility (e.g., Reuters, BBC).
        Summarize: Provide one 50-75 word summary per article, focusing on actionable insights.
        Articles: {json.dumps(articles)}
        Output: Strict JSON starting with '{{' and ending with '}}' with:
        - 'summaries': List of 50-75 word summaries, one per prioritized article, matching 'data' order and count (up to 5).
        - 'data': List of {'id', 'source'} objects for prioritized articles.
        Example: {{"summaries": ["Insight for article 1...", "Insight for article 2..."], "data": [{{"id": "uuid1", "source": "Source1"}}, {{"id": "uuid2", "source": "Source2"}}]}}
        If <5 articles, match 'summaries' and 'data' counts. If none, return {{"summaries": [], "data": [], "note": "No relevant articles"}}.
        No text outside JSON.
        """

        # Call OpenAI API with the new client
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a coffee procurement expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.5
            )
            result = response.choices[0].message.content
            result_json = json.loads(result)
            # Save successful response
            ProcurementNewsSummary.objects.create(result_json=result_json)
            return Response(result_json, status=status.HTTP_200_OK)
        except json.JSONDecodeError as e:
            # Fetch the latest saved response on failure
            latest_summary = ProcurementNewsSummary.objects.first()
            if latest_summary:
                print(f"Using cached response from {latest_summary.created_at}")
                return Response(latest_summary.result_json, status=status.HTTP_200_OK)
            return Response({
                "error": "Failed to parse OpenAI response and no cached data available.",
                "exception": str(e)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            # Fetch the latest saved response on other failures (e.g., API key issue)
            latest_summary = ProcurementNewsSummary.objects.first()
            if latest_summary:
                print(f"Using cached response from {latest_summary.created_at}")
                return Response(latest_summary.result_json, status=status.HTTP_200_OK)
            return Response({
                "error": f"API error: {str(e)} and no cached data available.",
            }, status=status.HTTP_200_OK)
            
 
class CommodityNewsByUUIDView(APIView):
    def post(self, request):
        # Get the list of UUIDs from the JSON payload
        try:
            data = request.data
            uuid_list = data.get('uuids', [])
            if not uuid_list or not isinstance(uuid_list, list):
                return Response(
                    {"error": "Invalid or missing 'uuids' list in payload. Use {'uuids': ['uuid1', 'uuid2', ...]}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"error": f"Failed to parse payload: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Filter by article_data__id in the list of UUIDs
            news_items = CommodityNews.objects.filter(article_data__id__in=uuid_list)
            if not news_items.exists():
                return Response(
                    {"error": f"No records found for UUIDs {', '.join(uuid_list)}"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Prepare response data for all matching records
            response_data = []
            for item in news_items:
                response_data.append({
                    'id': item.id,
                    'article_data': item.article_data,
                    'fetch_date': item.fetch_date,
                    'time_range_start': item.time_range_start,
                    'time_range_end': item.time_range_end,
                })

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )