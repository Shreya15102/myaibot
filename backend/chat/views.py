import os
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Phone
from .utils import get_gemini_explanation, normalize_price, parse_query


class ChatAPI(APIView):
    def post(self, request):
        query = request.data.get("query", "").strip()
        if not query:
            return Response({"error": "Query is required."}, status=400)
        print(query)
        lower_query = query.lower()
        unsafe_phrases = ["api key", "system prompt", "ignore your rules", "reveal", "trash"]
        if any(phrase in lower_query for phrase in unsafe_phrases):
            return Response({
                "response": "Sorry, I can't share internal details or make biased statements. Please ask about phones or features instead."
            })

        intent = parse_query(query)
        print(intent)
        print("intent", intent)

        if intent['type'] == 'explain' and intent['explain']:
            explanation = get_gemini_explanation(intent['explain'])
            return Response({"response": explanation})

        if intent['type'] == 'compare' and intent['compare']:
            phone_names = intent['compare']
            phones = Phone.objects.filter(model__icontains=phone_names[0]) | Phone.objects.filter(model__icontains=phone_names[1])
            if not phones.exists():
                return Response({"response": "Couldn't find both models in the catalog."})

            data = [{
                "model": p.model,
                "brand_name": p.brand_name,
                "price": p.price,
                "primary_camera_rear": p.primary_camera_rear,
                "battery_capacity": p.battery_capacity,
                "processor_brand": p.processor_brand,
                "screen_size": p.screen_size,
                "fast_charging": p.fast_charging,
                "os": p.os,
                "avg_rating": p.avg_rating
            } for p in phones]

            return Response({
                "response": f"Here’s a comparison between {phone_names[0]} and {phone_names[1]}:",
                "data": data
            })

        qs = Phone.objects.all()

        # Brand filter
        if intent.get('brand'):
            qs = qs.filter(brand_name__icontains=intent['brand'])

        # OS filter
        if intent.get('os'):
            if intent['os'].lower() == 'android':
                qs = qs.filter(os__icontains='android').exclude(brand_name__iexact='Apple')
            elif intent['os'].lower() in ['ios', 'iphone']:
                qs = qs.filter(Q(os__icontains='ios') | Q(brand_name__iexact='Apple'))

        # Budget filter
        budget_value = intent.get('budget')
        if budget_value:
            qs = qs.filter(price__lte=budget_value)

        # Feature-based filtering
        feature = intent.get('feature')
        if feature == 'camera':
            qs = qs.filter(Q(primary_camera_rear__gte=108) | Q(primary_camera_front__gte=200)).order_by('-avg_rating')
        elif feature == 'battery':
            qs = qs.filter(Q(battery_capacity__gte=5000) | Q(battery_capacity__gte=6000)).order_by('-avg_rating')
        elif feature == 'compact':
            qs = qs.filter(Q(screen_size__lte=6.2)).order_by('-avg_rating')

        # Best or top query prioritization
        else:
            qs = qs.order_by('-avg_rating')

        phones = qs[:3]
        if not phones.exists():
            return Response({"response": "Sorry, I couldn't find matching phones for your query."})

        data = [{
            "model": p.model,
            "brand_name": p.brand_name,
            "price": p.price,
            "screen_size": p.screen_size,
            "processor_brand": p.processor_brand,
            "ram_capacity": p.ram_capacity,
            "internal_memory": p.internal_memory,
            "primary_camera_rear": p.primary_camera_rear,
            "primary_camera_front": p.primary_camera_front,
            "battery_capacity": p.battery_capacity,
            "fast_charging": p.fast_charging,
            "os": p.os,
            "is_5g": p.is_5g,
            "avg_rating": p.avg_rating
        } for p in phones]

        rationale = "Phones are recommended based on high ratings and matching your preferences"
        if intent.get('budget'):
            rationale += f" under ₹{intent['budget']}."
        if intent.get('feature'):
            rationale += f" Optimized for {intent['feature']} performance."

        return Response({
            "response": rationale,
            "data": data
        })
