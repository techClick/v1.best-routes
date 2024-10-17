from django.shortcuts import HttpResponse
from .utils import get_nodes

# Create your views here.
@api_view(['POST'])
def get_routes(request):
  # r = get_nodes((-80, 35), (-70, 40))
  data = request.POST
  action = data.get("source")
  r = get_nodes((-83.920699, 35.96061), (-73.973846, 40.71742))
  return HttpResponse(r)
