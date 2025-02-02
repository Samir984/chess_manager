from django.core.cache import cache
from django.http import JsonResponse, HttpRequest
from django.http.response import HttpResponse
from typing import Callable

class RateLimitMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        print(request.path)
        if request.path == "/api/reports/": 
            ip = request.META.get("REMOTE_ADDR", "")
            key = f"ratelimit:{ip}:report"  #
            print("middle",ip,key)
 
            request_count = cache.get(key, 0)

           
            if request_count >= 2:  # Allow 2 requests per minute
                return JsonResponse({"detail": "Rate limit exceeded. Try again later."}, status=429)
            
            cache.set(key, request_count + 1, timeout=60) 

        return self.get_response(request)
