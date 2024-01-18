from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import Use_Miso, Used_Miso
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

# ユーザー登録
# class RegistForm(forms.ModelForm):
#     username = forms.CharField(label='名前')
#     email = forms.EmailField(label='メールアドレス')
#     password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    
#     class Meta:
#         model = Users
#         fields = ['username', 'email', 'password']
        
#     def save(self, commit=False):
#         user = super().save(commit=False) 
#         validate_password(self.cleaned_data['password'], user)
#         user.set_password(self.cleaned_data['password'])
#         user.save()
#         return user   

#ユーザー登録    
Users = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='メールアドレス')

    class Meta:
        model = Users
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password1'], user)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
        
        
# ユーザーログイン
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())    
 
 
#パスワード変更
class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = Users
 
 
# 使いたい味噌
class Use_MisoForm(forms.ModelForm):
    class Meta:
        model = Use_Miso 
        fields = ['name', 'image']
        labels = {
            'name': '商品名',
            'image': '商品画像',
        }
    

# 使った味噌    
class Used_MisoForm(forms.ModelForm):
    class Meta:
        model = Used_Miso
        fields = ['name', 'image', 'thoughts', 'taste_rating', 'appearance_rating']
        labels = {
            'name': '商品名',
            'image': '商品画像',
            'thoughts': '感想',
            'taste_rating': '味の評価',
            'appearance_rating': '見た目の評価',
            
        }


class ToggleFavoriteForm(forms.Form):
    # お気に入りのトグルに関連するフォームの定義
    pass  # 必要に応じてフィールドを追加