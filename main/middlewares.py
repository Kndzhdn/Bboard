from .models import SubRubric
#keyword - переменная для генерирования интернет-адресов в гиперссылках пагинатора
#all - переменная с GET-параметрами keyword и page, которые добавляются к интернет-адресам гиперссылок, указывающих на страницы сведений об объявлениях
def bboard_context_processor(request):
	context = {}
	context['rubrics'] = SubRubric.objects.all()
	context['keyword'] = ''
	context['all'] = ''
	if 'keyword' in request.GET:
		keyword = request.GET['keyword']
		if keyword:
			context['keyword'] = '?keyword=' + keyword
			context['all'] = context['keyword']
	if 'page' in request.GET:
		page = request.GET['page']
		if page != '1':
			if context['all']:
				context['all'] += '&page' + page
			else:
				context['all'] = '?page=' + page
	return context
