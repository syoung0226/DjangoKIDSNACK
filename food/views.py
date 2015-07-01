# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from food.models import Snack, SnackHate, SnackLike, Additive, RequireSnack
from food.forms import TokenCheckForm, SnackIdCheckForm, ListIndexCheckForm
from django.views.decorators.csrf import csrf_exempt

Nothing = 0
Like = 1
Hate = 2


def snack_preference(form, snack):
    preference = Nothing
    if SnackLike.objects.filter(snack=snack, user=form.get_user()):
        preference = Like
    if SnackHate.objects.filter(snack=snack, user=form.get_user()):
        preference = Hate
    return preference


def cal_count_grade(snack):
    # DB 저장 (유해성분 갯수, 스낵 등급, 부작용 갯수)
    toxic_ingredients = Additive.objects.filter(snack=snack, toxic_ingredient_check=True)
    snack.toxic_ingredient_count = len(toxic_ingredients)

    if snack.toxic_ingredient_count == 0:
        return

    sum_toxic_ingredient_grade = 0
    total_side_effects = []

    for toxic_ingredient in toxic_ingredients:
        sum_toxic_ingredient_grade = sum_toxic_ingredient_grade + toxic_ingredient.grade
        total_side_effects = total_side_effects + toxic_ingredient.side_effect_to_dict()

    snack.snack_grade = sum_toxic_ingredient_grade / snack.toxic_ingredient_count
    snack.side_effect_count = len(list(set(total_side_effects)))
    snack.save()


@csrf_exempt
def snack_list(request):
    form = ListIndexCheckForm(request.POST)
    if form.is_valid():
        index = form.cleaned_data['index']
        db_snacks = Snack.objects.all()
        snacks = db_snacks.order_by('-snack_grade')[index:index+20]
        total_count = len(db_snacks)
        for snack in snacks:
            snack.preference = snack_preference(form, snack)
            #cal_count_grade(snack)
        return HttpResponse(json.dumps(dict(status=dict(title="MainSnackList", code='OK', reason='OK'),
                                            totalCount=total_count,
                                            snacks=[snack.list_to_dict() for snack in snacks])),
                            content_type="application/json")
    return HttpResponse(json.dumps(dict(status=dict(title="MainSnackList", code="FAIL",
                                                    reason=form.errors.keys()[0]))), content_type='application/json')


@csrf_exempt
def snack_detail(request):
    form = SnackIdCheckForm(request.POST)
    if form.is_valid():
        snack = form.get_snack()
        snack.preference = snack_preference(form, snack)

        #cal_count_grade(snack)

        return HttpResponse(json.dumps(dict(status=dict(title="SnackDetail", code='OK', reason='OK'),

                                            snack=snack.detail_to_dict())),
                            content_type="application/json")
    return HttpResponse(json.dumps(dict(status=dict(title="SnackDetail", code="FAIL", reason=form.errors.keys()[0]))),
                        content_type='application/json')


@csrf_exempt
def snack_compare(request):
    form = SnackIdCheckForm(request.POST)
    if form.is_valid():
        snack = form.get_snack()
        snack.preference = snack_preference(form, snack)

        #cal_count_grade(snack)

        return HttpResponse(json.dumps(dict(status=dict(title="SnackCompare", code='OK', reason='OK'),
                                            snack=snack.detail_to_dict())),
                            content_type="application/json")
    return HttpResponse(json.dumps(dict(status=dict(title="SnackCompare", code="FAIL", reason=form.errors.keys()[0]))),
                        content_type='application/json')


@csrf_exempt
def snack_search(request):
    form = ListIndexCheckForm(request.POST)
    snack_name = request.POST['snackName']
    if form.is_valid():
        index = form.cleaned_data['index']
        try:
            db_snacks = Snack.objects.filter(name__contains=snack_name)
            snacks = db_snacks.order_by('-snack_grade')[index:index+20]
            #snacks = db_snacks[index:index+20]
            total_count = len(db_snacks)
            for snack in snacks:
                snack.preference = snack_preference(form, snack)
                #cal_count_grade(snack)
        except Snack.DoesNotExist:
            return HttpResponse(json.dumps(dict(status=dict(title="SnackSearch", code='FAIL',
                                                            reason=u'존재하지 않는 식품입니다.'))),
                                content_type="application/json")
        return HttpResponse(json.dumps(dict(status=dict(title="SnackSearch", code='OK', reason='OK'),
                                            totalCount=total_count,
                                            snacks=[snack.list_to_dict() for snack in snacks])),
                            content_type="application/json")
    return HttpResponse(json.dumps(dict(status=dict(title="SnackSearch", code="FAIL", reason=form.errors.keys()[0]))),
                        content_type='application/json')


@csrf_exempt
def snack_like_list(request):
    form = ListIndexCheckForm(request.POST)
    if form.is_valid():
        index = form.cleaned_data['index']
        db_snacks_like = SnackLike.objects.filter(user=form.get_user())
        snacks_like = db_snacks_like[index:index+20]
        #snacks_hate = db_snacks.order_by('-snack_grade')[index:index+20]
        total_count = len(db_snacks_like)
        return HttpResponse(json.dumps(dict(status=dict(title="SnackLikeList", code='OK', reason='OK'),
                                            totalCount=total_count,
                                            snacks=[_snack_like.list_to_dict() for _snack_like in snacks_like])),
                            content_type="application/json")
    return HttpResponse(json.dumps(dict(status=dict(title="SnackLikeList", code="FAIL", reason=form.errors.keys()[0]))),
                        content_type='application/json')


@csrf_exempt
def snack_hate_list(request):
    form = ListIndexCheckForm(request.POST)
    if form.is_valid():
        index = form.cleaned_data['index']
        db_snacks_hate = SnackHate.objects.filter(user=form.get_user())
        snacks_hate = db_snacks_hate[index:index+20]
        #snacks_hate = db_snacks.order_by('-snack_grade')[index:index+20]
        total_count = len(db_snacks_hate)

        return HttpResponse(json.dumps(dict(status=dict(title="SnackHateList", code='OK', reason='OK'),
                                            totalCount=total_count,
                                            snacks=[_snack_hate.list_to_dict() for _snack_hate in snacks_hate])),
                            content_type="application/json")
    return HttpResponse(json.dumps(dict(status=dict(title="SnackHateList", code="FAIL", reason=form.errors.keys()[0]))),
                        content_type='application/json')


@csrf_exempt
def snack_like(request):
    form = SnackIdCheckForm(request.POST)
    if form.is_valid():
        snack = form.get_snack()
        SnackHate.objects.filter(snack=snack, user=form.get_user()).delete()
        try:
            SnackLike.objects.get(snack=snack, user=form.get_user())
        except SnackLike.DoesNotExist:
            new_snack_like = SnackLike(snack=snack, user=form.get_user())
            new_snack_like.save()
            return HttpResponse(json.dumps(dict(status=dict(title="SnackLike", code='OK', reason='OK'))),
                                content_type="application/json")

        return HttpResponse(json.dumps(dict(status=dict(title="SnackLike", code="FAIL",
                                                        reason=u'이미 좋아요 리스트에 있는 제품입니다.'))),
                            content_type='application/json')
    return HttpResponse(json.dumps(dict(status=dict(title="SnackLike", code="FAIL", reason=form.errors.keys()[0]))),
                        content_type='application/json')


@csrf_exempt
def snack_hate(request):
    form = SnackIdCheckForm(request.POST)
    if form.is_valid():
        snack = form.get_snack()
        SnackLike.objects.filter(snack=snack, user=form.get_user()).delete()
        try:
            SnackHate.objects.get(snack=snack, user=form.get_user())
        except SnackHate.DoesNotExist:
            new_snack_hate = SnackHate(snack=snack, user=form.get_user())
            new_snack_hate.save()
            return HttpResponse(json.dumps(dict(status=dict(title="SnackHate", code='OK', reason='OK'))),
                                content_type="application/json")

        return HttpResponse(json.dumps(dict(status=dict(title="SnackHate", code="FAIL",
                                                        reason=u'이미 싫어요 리스트에 있는 제품입니다.'))),
                            content_type='application/json')
    return HttpResponse(json.dumps(dict(status=dict(title="SnackHate", code="FAIL", reason=form.errors.keys()[0]))),
                        content_type='application/json')


@csrf_exempt
def snack_like_del(request):
    form = SnackIdCheckForm(request.POST)
    if form.is_valid():
        snack = form.get_snack()
        try:
            SnackLike.objects.get(snack=snack, user=form.get_user()).delete()
        except SnackLike.DoesNotExist:
            return HttpResponse(json.dumps(dict(status=dict(title="SnackLikeDel", code="FAIL",
                                                            reason=u'좋아요 리스트에 존재하지 않은 식품입니다.'))),
                                content_type='application/json')
        return HttpResponse(json.dumps(dict(status=dict(title="SnackLikeDel", code='OK', reason='OK del'))),
                            content_type="application/json")
    return HttpResponse(json.dumps(dict(status=dict(title="SnackLikeDel", code="FAIL", reason=form.errors.keys()[0]))),
                        content_type='application/json')


@csrf_exempt
def snack_hate_del(request):
    form = SnackIdCheckForm(request.POST)
    if form.is_valid():
        snack = form.get_snack()
        try:
            SnackHate.objects.get(snack=snack, user=form.get_user()).delete()
        except SnackHate.DoesNotExist:
            return HttpResponse(json.dumps(dict(status=dict(title="SnackHateDel", code="FAIL",
                                                            reason=u'싫어요 리스트에 존재하지 않은 식품입니다.'))),
                                content_type='application/json')
        return HttpResponse(json.dumps(dict(status=dict(title="SnackHateDel", code='OK', reason='OK del'))),
                            content_type="application/json")
    return HttpResponse(json.dumps(dict(status=dict(title="SnackHateDel", code="FAIL", reason=form.errors.keys()[0]))),
                        content_type='application/json')


@csrf_exempt
def snack_like_del_all(request):
    form = TokenCheckForm(request.POST)
    if form.is_valid():
        SnackLike.objects.filter(user=form.get_user()).delete()
        return HttpResponse(json.dumps(dict(status=dict(title="SnackLikeAllDel", code='OK', reason='OK all del'))),
                            content_type="application/json")
    return HttpResponse(json.dumps(dict(status=dict(title="SnackLikeAllDel", code="FAIL",
                                                    reason=form.errors.keys()[0]))), content_type='application/json')


@csrf_exempt
def snack_hate_del_all(request):
    form = TokenCheckForm(request.POST)
    if form.is_valid():
        SnackHate.objects.filter(user=form.get_user()).delete()
        return HttpResponse(json.dumps(dict(status=dict(title="SnackHateAllDel", code='OK', reason='OK all del'))),
                            content_type="application/json")
    return HttpResponse(json.dumps(dict(status=dict(title="SnackHateAllDel", code="FAIL",
                                                    reason=form.errors.keys()[0]))), content_type='application/json')


@csrf_exempt
def snack_name_auto_complete(request):
    form = TokenCheckForm(request.POST)
    snack_name = request.POST['snackName']
    if form.is_valid():
        snacks = Snack.objects.filter(name__contains=snack_name)[0:20]
        return HttpResponse(json.dumps(dict(status=dict(title="SnackNameAutoComplete", code='OK', reason='OK'),
                                            snacks=[snack.name for snack in snacks])),
                            content_type="application/json")
    return HttpResponse(json.dumps(dict(status=dict(title="SnackNameAutoComplete", code="FAIL",
                                                    reason=form.errors.keys()[0]))), content_type='application/json')


@csrf_exempt
def snack_require(request):
    form = TokenCheckForm(request.POST)
    snack_name = request.POST['snackName']
    snack_brand_name = request.POST['brandName']
    if form.is_valid():
        new_require_snack = RequireSnack(name=snack_name, brand=snack_brand_name, user=form.get_user())
        new_require_snack.save()
        return HttpResponse(json.dumps(dict(status=dict(title="RequireSnack", code='OK', reason='OK'))),
                            content_type="application/json")
    return HttpResponse(json.dumps(dict(status=dict(title="RequireSnack", code="FAIL", reason=form.errors.keys()[0]))),
                        content_type='application/json')
