from django.shortcuts import render
from django.core.paginator import Paginator
from ..models import Question
from django.db.models import Q

import logging
logger = logging.getLogger('__name__')

def index(request):
    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")
    logger.info("INFO 레벨로 출력")
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '') #검색어

    question_list = Question.objects.order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(answer__content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj , 'page' : page , 'kw': kw }
    return render(request , 'pybo/question_list.html', context)


def detail(request , question_id):
    question = Question.objects.get(id=question_id)
    context = {'question':question}
    return render(request , 'pybo/question_detail.html', context)