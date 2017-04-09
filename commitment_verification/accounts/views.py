from django.contrib.auth.views import login as auth_login
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render
from .forms import LoginForm

def login(request):
    providers = []
    for provider in get_providers(): # settings/INSTALLED_APPS 내에서 활성화된 목록
    # social_app속성은 provider에는 없는 속성입니다.
        try:
            # 실제 Provider별 Client id/secret 이 등록이 되어있는가?
            provider.social_app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)
        except SocialApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)

    return auth_login(request,
        #authentication_form=LoginForm,
        template_name='accounts/login_form.html',
        extra_context={'providers': providers})


@login_required
def profile(request):
 return render(request, 'accounts/profile.html')
