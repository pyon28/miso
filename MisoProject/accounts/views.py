from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView, View
from .forms import UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import Use_Miso, Used_Miso
from .forms import (Use_MisoForm, Used_MisoForm, CustomUserCreationForm, 
CustomPasswordChangeForm) 
from django.views import View
from .models import Product
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import PasswordChangeView
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Used_Miso
from .forms import Use_MisoForm, Used_MisoForm
import logging


# ホーム
class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    

# 管理者 
def is_admin(user):
    return user.is_authenticated and user.is_staff

admin_required = user_passes_test(is_admin)

@method_decorator(admin_required, name='dispatch')    
class AuthorityView(View):
    template_name = 'authority.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   
        

# ユーザー登録
class RegistUserView(View):
    template_name = 'regist.html'
    form_class = CustomUserCreationForm 
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # フォームのバリデーションが成功した場合の処理
            user = form.save()  # ユーザーを保存
            login(request, user)  # ユーザーをログイン状態にする
            return redirect('accounts:home')  # ホームページにリダイレクト
           

        return render(request, self.template_name, {'form': form})


# ユーザーログイン    
class UserLoginView(LoginView):
    template_name = 'user_login.html'
    # authentication_from = UserLoginForm
        
    success_url = reverse_lazy('accounts:home')  # ログイン成功後のリダイレクト先

    def form_valid(self, form):
        response = super().form_valid(form)
        # ログイン成功時の追加の処理があればここに追加
        return response
    
    def form_invalid(self, form):
        return super().form_invalid(form)
     

#ユーザー    
class UserView(TemplateView):
    template_name = 'user.html'    
    
    @method_decorator(login_required)
    def dispatch(self, *args,**kwargs):
        return super().dispatch(*args, **kwargs) 
      

# ユーザーログアウト
class UserLogoutView(LogoutView):
    pass

#パスワード変更
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('accounts:my_page')  # パスワード変更成功後のリダイレクト先

@login_required
def password_change(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:my_page')  # 成功したらマイページにリダイレクト
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'password_change.html', {'form': form})



# 商品一覧
# class ProductListView(View):
#     template_name = 'product_list.html'

#     def get(self, request, *args, **kwargs):
#         use_misos = Use_Miso.objects.all()
#         used_misos = Used_Miso.objects.all()

#         use_form = Use_MisoForm()
#         used_form = Used_MisoForm()

#         return render(request, self.template_name, {'use_misos': use_misos, 'used_misos': used_misos, 'use_form': use_form, 'used_form': used_form})

#     def post(self, request, *args, **kwargs):
#         use_form = Use_MisoForm(request.POST, request.FILES)
#         used_form = Used_MisoForm(request.POST, request.FILES)

#         if use_form.is_valid():
#             use_form.save()
#         elif used_form.is_valid():
#             used_form.save()
#             return redirect('accounts:product_list')  # 商品一覧ページにリダイレクト

#         # フォームが無効な場合は、再度商品一覧ページを表示
#         use_misos = Use_Miso.objects.all()
#         used_misos = Used_Miso.objects.all()

#         return render(request, self.template_name, {'use_misos': use_misos, 'used_misos': used_misos, 'use_form': use_form, 'used_form': used_form})


#商品一覧
class ProductListView(View):
    template_name = 'product_list.html'

    def get(self, request, *args, **kwargs):
        use_misos = Use_Miso.objects.all()
        used_misos = Used_Miso.objects.all()
        use_form = Use_MisoForm()
        used_form = Used_MisoForm()
        
        # お気に入り状態を取得してコンテキストに追加
        favorites = Used_Miso.objects.filter(favorites=request.user)

        return render(request, self.template_name, {
            'use_misos': use_misos,
            'used_misos': used_misos,
            'use_form': use_form,
            'used_form': used_form,
            'favorites': favorites,
        })

    def post(self, request, *args, **kwargs):
        use_form = Use_MisoForm(request.POST, request.FILES)
        used_form = Used_MisoForm(request.POST, request.FILES)

        if use_form.is_valid():
            use_form.save()
        elif used_form.is_valid():
            used_form.save()

            # お気に入り機能のトグル
            miso_pk = used_form.instance.pk
            self.toggle_favorite(request, miso_pk)

        

            return redirect('accounts:product_list')  # 商品一覧ページにリダイレクト

        # フォームが無効な場合は、再度商品一覧ページを表示
        use_misos = Use_Miso.objects.all()
        used_misos = Used_Miso.objects.all()

        return render(request, self.template_name, {
            'use_misos': use_misos,
            'used_misos': used_misos,
            'use_form': use_form,
            'used_form': used_form,
        })

    def toggle_favorite(self, request, pk):
        miso = Used_Miso.objects.get(pk=pk)
        user = request.user

        if miso.favorites.filter(pk=user.id).exists():
            miso.favorites.remove(user)
        else:
            miso.favorites.add(user)

        # リクエストのGETパラメータからリダイレクト先のURLを取得
        redirect_url = request.GET.get('next', 'accounts:my_page')

        return redirect(redirect_url)


@method_decorator(login_required, name='dispatch')
class ToggleFavoriteView(View):
    def get(self, request, pk):
        miso = get_object_or_404(Used_Miso, pk=pk)
        user = request.user

        # お気に入りのトグル
        if miso.favorites.filter(pk=user.id).exists():
            miso.favorites.remove(user)
        else:
            miso.favorites.add(user)

        # デバッグログを追加
        logger = logging.getLogger(__name__)
        logger.debug('ToggleFavoriteView get method called')

        # リダイレクト先のURLを取得
        redirect_url = request.GET.get('next', 'accounts:my_page')
        
        # ログに出力
        logging.debug(f'Redirecting to: {redirect_url}')


        # リダイレクト
        return redirect(redirect_url)
        

# import logging       
# @method_decorator(login_required, name='dispatch')
# class MyFavoriteView(View):
#     template_name = 'my_favorite.html'

#     def get(self, request):
#         logger = logging.getLogger(__name__)
#         logging.debug('MyFavoriteView get method called')  # ログを追加

#         # ログインユーザーのお気に入り商品を取得
#         favorites = Used_Miso.objects.filter(favorites=request.user)
        
#         return render(request, self.template_name, {'favorites': favorites})

# class MyFavoriteView(View):
#     template_name = 'my_favorite.html'

#     def get(self, request):
#         print('MyFavoriteView get method called')  # デバッグ用の出力
        
        
#         # ログインユーザーのお気に入り商品を取得
#         favorites = Used_Miso.objects.filter(favorites=request.user)
        
#         return render(request, self.template_name, {'favorites': favorites})    

    
logger = logging.getLogger(__name__)

class MyFavoriteView(View):
    template_name = 'my_favorite.html'

    def get(self, request):
        # ログを追加
        logger.debug('MyFavoriteView get method called')

        # ログにお気に入りデータを表示
        favorites = Used_Miso.objects.filter(favorites=request.user)
        logger.debug(f'Favorites: {favorites}')

        # テンプレートにデータを渡す
        return render(request, self.template_name, {'favorites': favorites})    
            
            
#使いたい味噌　編集    
class EditUseView(View):
    template_name = 'edit_use.html'  # 編集画面のテンプレート名に合わせて変更

    def get(self, request, pk):
        use_miso = get_object_or_404(Use_Miso, pk=pk)  # モデルに合わせて変更
        form = Use_MisoForm(instance=use_miso)  # フォームに合わせて変更
        return render(request, self.template_name, {'form': form, 'pk': pk})

    def post(self, request, pk):
        use_miso = get_object_or_404(Use_Miso, pk=pk)  # モデルに合わせて変更
        form = Use_MisoForm(request.POST, instance=use_miso)  # フォームに合わせて変更
        if form.is_valid():
            form.save()
            return redirect('accounts:product_list')  # 編集後に商品一覧にリダイレクト

        return render(request, self.template_name, {'form': form, 'pk': pk})


#使った味噌 編集
class EditUsedView(View):
    template_name = 'edit_used.html'  # 編集画面のテンプレート名に合わせて変更

    def get(self, request, pk):
        used_miso = get_object_or_404(Used_Miso, pk=pk)  # モデルに合わせて変更
        form = Used_MisoForm(instance=used_miso)  # フォームに合わせて変更
        return render(request, self.template_name, {'form': form, 'pk': pk})

    def post(self, request, pk):
        used_miso = get_object_or_404(Used_Miso, pk=pk)  # モデルに合わせて変更
        form = Used_MisoForm(request.POST, instance=used_miso)  # フォームに合わせて変更
        if form.is_valid():
            form.save()
            return redirect('accounts:product_list')  # 編集後に商品一覧にリダイレクト

        return render(request, self.template_name, {'form': form, 'pk': pk})


#使いたい味噌 削除
class DeleteUseView(View):
    template_name = 'delete_use.html'  # 確認画面のテンプレート名に合わせて変更

    def get(self, request, pk):
        use_miso = get_object_or_404(Use_Miso, pk=pk)  # モデルに合わせて変更
        return render(request, self.template_name, {'use_miso': use_miso})

    def post(self, request, pk):
        use_miso = get_object_or_404(Use_Miso, pk=pk)  # モデルに合わせて変更
        use_miso.delete()
        return redirect('accounts:product_list')  # 削除後に商品一覧にリダイレクト



#使った味噌 削除
class DeleteUsedView(View):
    template_name = 'delete_used.html'  # 確認画面のテンプレート名に合わせて変更

    def get(self, request, pk):
        used_miso = get_object_or_404(Used_Miso, pk=pk)  # モデルに合わせて変更
        return render(request, self.template_name, {'used_miso': used_miso})

    def post(self, request, pk):
        used_miso = get_object_or_404(Used_Miso, pk=pk)  # モデルに合わせて変更
        used_miso.delete()
        return redirect('accounts:product_list')  # 削除後に商品一覧にリダイレクト



# 使いたい味噌
class Use_MisoView(View):
    template_name = 'use_miso.html'   
    
    def get(self, request):
        use_form = Use_MisoForm()
        return render(request, self.template_name, {'use_form': use_form})

    def post(self, request):
        use_form = Use_MisoForm(request.POST, request.FILES)
        if use_form.is_valid():
            use_form.save()
        return redirect('accounts:product_list')  #  商品一覧ページにリダイレクト

        
# 使った味噌
class Used_MisoView(View):
    template_name = 'used_miso.html'   
    
    def get(self, request):
        used_form = Used_MisoForm()
        return render(request, self.template_name, {'used_form': used_form})

    def post(self, request):
        used_form = Used_MisoForm(request.POST, request.FILES)
        if used_form.is_valid():
            used_form.save()
        return redirect('accounts:product_list')  # 商品一覧ページにリダイレクト


    
# 商品登録
class ProductRegistrationView(View):
    template_name = 'product_registration.html'
    login_url = 'user_login.html'  # ログインページのURLに置き換えてください

    def get(self, request, *args, **kwargs):
        use_form = Use_MisoForm()
        used_form = Used_MisoForm()
        use_list = Use_Miso.objects.all()
        used_list = Used_Miso.objects.all()
        
        return render(request, self.template_name, {
            'use_form': use_form,
            'used_form': used_form,
            'use_list': use_list,
            'used_list': used_list,
        })

    def post(self, request, *args, **kwargs):
        use_form = Use_MisoForm()
        used_form = Used_MisoForm()
        use_list = Use_Miso.objects.all()
        used_list = Used_Miso.objects.all()

        if 'use_submit' in request.POST:
            use_form = Use_MisoForm(request.POST, request.FILES)
            if use_form.is_valid():
                use_form.save()
        elif 'used_submit' in request.POST:
            used_form = Used_MisoForm(request.POST, request.FILES)
            if used_form.is_valid():
                used_form.save()
        
        return render(request, self.template_name, {
            'use_form': use_form,
            'used_form': used_form,
            'use_list': use_list,
            'used_list': used_list,
        })
        

class SaveAsUsedView(View):
    template_name = 'accounts/save_as_used.html'  # テンプレートファイルが必要な場合は指定
    success_url = reverse_lazy('accounts:product_list')

    def get(self, request, pk):
        use_miso = get_object_or_404(Use_Miso, pk=pk)

        Used_Miso.objects.create(
            name=use_miso.name,
            image=use_miso.image,
            # comment=use_miso.comment,
            thoughts="",  # 適切な値をセット
            taste_rating=0,  # 適切な値をセット
            appearance_rating=0,  # 適切な値をセット
        )

        use_miso.delete()

        return redirect(self.success_url)





# マイページ
# @method_decorator(login_required, name='dispatch')
# class MyPageView(View):
#     template_name = 'my_page.html'

#     def get(self, request, *args, **kwargs):
#         # ログインユーザーのお気に入り商品を取得
#         favorites = Used_Miso.objects.filter(favorites=request.user)
        
        # 必要な商品情報を取得してコンテキストに追加
        # favorite_info = [{'name': miso.name, 'image': miso.image, 'taste_rating': miso.taste_rating,
        #                   'appearance_rating': miso.appearance_rating,
        #                   } for miso in favorites]

        # return render(request, self.template_name, {'favorites': favorites})

# views.py

class MyPageView(View):
    template_name = 'my_page.html'

    def get(self, request, *args, **kwargs):
        favorites = Used_Miso.objects.filter(favorites=request.user)
        
        return render(request, self.template_name, {
            'favorites': favorites,
        })




