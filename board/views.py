from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'title': 'Board list',
        'board_list': [
            {'no':1, 'title': '목록1' },
            {'no':2, 'title': '목록2' },
            {'no':3, 'title': '목록3' },
            {'no':4, 'title': '목록4' },
            {'no':5, 'title': '목록5' }
        ]
    }
    return render(request, 'board/index.html', context)