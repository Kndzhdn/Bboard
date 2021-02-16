from django.shortcuts import render


from rest_framework.response import Response
from rest_framework.decorators import api_view
from main.models import Bb
from .serializers import BbSerializer
#контроллёр, выдающий список объявлений
@api_view(['GET'])
def bbs(request):
	if request.method == 'GET':
		bbs = Bb.objects.filter(is_active=True)[:10]
		serializer = BbSerializer(bbs, many=True)
		return Response(serializer.data)






from rest_framework.generics import RetrieveAPIView
from .serializers import BbDetailSerializer
#контроллёр, выдающий сведения о выбранном объявлении
class BbDetailView(RetrieveAPIView):
	queryset = Bb.objects.filter(is_active=True)
	serializer_class = BbDetailSerializer








from rest_framework.decorators import permission_classes
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from main.models import Comment
from .serializers import CommentSerializer
#контроллёр, выдающий список комментариев и добавляющий новый комментарий
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def comments(request, pk):
	if request.method == 'POST':
		serializer = CommentSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
	else:
		comments = Comment.objects.filter(is_active=True, bb=pk)
		serializer = CommentSerializer(comments, many=True)
		return Response(serializer.data)
		