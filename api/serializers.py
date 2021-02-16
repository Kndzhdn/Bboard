from rest_framework import serializers
from main.models import Bb
#сериализатор, формирующий список объявлений
class BbSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bb
		fields = (
			'id',
			'title',
			'content',
			'price',
			'created_at'
		)


#сериализатор, выдающий сведения об объявлении
class BbDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bb
		fields = (
			'id',
			'title',
			'content',
			'price',
			'created_at',
			'contacts',
			'image'
		) 





from main.models import Comment
#сериализатор, отправляющий список комментариев и добавляющий новый комментарий
class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = (
			'bb',
			'author',
			'content',
			'created_at'
		)