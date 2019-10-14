from django.http import JsonResponse
from django.db.models import F

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Level, CircuimstanceUser, AnswerLog
from api.serializers import LevelSerializer
from .decorators import is_logged_in, set_cookies

from datetime import datetime
from redis_leaderboard.wrapper import RedisLeaderboard

rdb = RedisLeaderboard('redis', 6379, 0)

@is_logged_in
@api_view(['GET'])
def ask(request):

    user = request.session['user']
    kuser, created = CircuimstanceUser.objects.get_or_create(user_id=user)
    # TODO: Send message to websocket on new user.

    if created:
        rdb.add('circuimstance', user, 1)

    level = Level.objects.filter(level=kuser.level)

    if len(level) > 0:
        serializer = LevelSerializer(level[0])
        return Response(serializer.data)
    else:
        return JsonResponse({'completed': True})


@is_logged_in
@api_view(['GET'])
def answer(request):
    answer = request.GET['answer']

    try:
        user = request.session['user']
        kuser = CircuimstanceUser.objects.get(user_id=user)
        level = Level.objects.get(level=kuser.level)


        AnswerLog.objects.create(
            user_id=user,
            anstime=datetime.now(),
            level=level.level,
            answer=answer
        )
            
        if answer == level.answer:

            score = kuser.level + 1
            rdb.add ('circuimstance', user, score)

            # Here we use an F expression : Read more about it in Django docs.
            kuser.level = F('level') + 1
            kuser.last_anstime = datetime.now()
            kuser.save()
            response = {'answer': 'Correct'}

        else:
            response = {'answer': 'Wrong'}

        return JsonResponse(response)

    except Exception as e:
        resp = {'Error': 'Internal Server Error'}
        return JsonResponse(resp, status=500)

'''
@is_logged_in
@api_view(['GET'])
def leaderboard(request):
    try:
        data = []
        kusers = CircuimstanceUser.objects.all()
        rank = 1
            
        for kuser in kusers:
            dict={}
            dict['user_id'] = kuser.user_id
            dict['rank'] = rank
            rank += 1
            data.append(dict)
            
            return JsonResponse({'data': data})
        
    except:
        resp = {'Error': 'Internal Server Error'}
        return JsonResponse(resp, status=500)



@is_logged_in
@api_view(['GET'])
def myrank(request):
    try:
        user = request.session.get('user', False)
        if user:
            rank = CircuimstanceUser.objects.get(user_id = user).rank
            return JsonResponse({'rank': rank})
        else:
            return JsonResponse({'Error': 'User not logged in'}, status=403)

    except:
        return JsonResponse({'Error': 'Internal Server Error'}, status=500)
'''
