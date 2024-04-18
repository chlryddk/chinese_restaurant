from django.shortcuts import render, redirect
from .models import Food
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

# 자신이 판매하는 상품 리스트를 보여주기
# -> 전체 Food에서 특정 user(판매자)인 food만 가져온다
# -> 전체 Food에서 내가 올린 food만 filter한다

# 상품 등록 기능

@login_required
def seller_index(request):
    # foods = Food.objects.all().filter(user__id=request.user.id) # 본인 user__id랑 request user id가 같은것만 뜨게 필터링
    foods = Food.objects.filter(user = request.user)
    context = {
        'object_list': foods
    }

    return render(request, 'seller/seller_index.html', context)

@login_required
def add_food(request):
    # get과 post로 나눠서 처리하자
    if request.method == 'GET':
        return render(request, 'seller/seller_add_food.html')
    elif request.method == 'POST':
        # form에서 전달하는 각 값을 뽑아와서 DB에 저장
        # food_name, price, description
        # category = Category.objects.get(name=request.POST['category']) # forign Key는 인스턴스로 가져와야함
        user = request.user
        food_name = request.POST['name']
        food_price = request.POST['price']
        food_description = request.POST['description']

        fs = FileSystemStorage()
        uploaded_file = request.FILES['file']
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)

        Food.objects.create(user=user, name=food_name, price=food_price, description = food_description, image_url = url)

        return redirect('seller:seller_index')

@login_required  
def food_detail(request,pk):
    food = Food.objects.get(pk=pk)

    context = {
        'object': food
    }

    return render(request, 'seller/seller_food_detail.html', context)

def food_delete(request,pk):
    object = Food.objects.get(pk=pk)
    object.delete()
    return redirect('seller:seller_index')