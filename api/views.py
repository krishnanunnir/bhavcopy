import datetime
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from .serializers import EquitySerializer
from .Pagination import PageNumberCountPagination
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['GET'])
def stock_list(request):
    """
    Returns an API with content of all the stocks
    since there is only one method, I don't think there is need for abstracts and such like viewsets
    """
    if request.method=="GET":
        paginator = PageNumberCountPagination()
        paginator.page_size = 200
        all_stocks = []
        # keys are not ideal in very large caches
        # but our db at max contains 3000 records corresponding to equity csv
        stock_list =  cache.keys("*")
        for stock in stock_list:
            all_stocks+=[cache.get(stock)]
        result_page = paginator.paginate_queryset(all_stocks, request)
        serializer = EquitySerializer(result_page,many= True)
        return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def stock_list_by_name(request, stockname):
    """
    Returns an API with content of the stock with name stockname
    Search is basic query with sql 'like', so not as accurate
    """
    if request.method=="GET":
        paginator = PageNumberCountPagination()
        paginator.page_size = 200
        search_result = []
        search_key = cache.keys("*"+stockname.lower() +"*")
        for key in search_key:
            search_result+=[cache.get(key)]
        result_page = paginator.paginate_queryset(search_result, request)
        serializer = EquitySerializer(result_page,many= True)
        return paginator.get_paginated_response(serializer.data)