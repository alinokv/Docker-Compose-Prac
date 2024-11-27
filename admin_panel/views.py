import io
import os
import string
import random
import subprocess
from datetime import datetime
from email.message import EmailMessage
#
# import pandas as pd
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from app import settings
from users.models import User, Role
from django.db.models import Q
import csv


def block_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    return redirect('admin-panel:user_list')


def unblock_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    return redirect('admin-panel:user_list')


class UserListView(ListView):
    model = User
    template_name = 'admin-panel/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        role = self.request.GET.get('role')
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        if role:
            queryset = queryset.filter(role__role_name=role)
        return queryset.order_by('role__role_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = Role.objects.all()  # Загружаем роли из модели Role
        return context


@require_POST
def change_user_role(request):
    user_id = request.POST.get('user_id')
    new_role_id = request.POST.get('role')

    if not user_id or not new_role_id:
        return redirect('admin-panel:user_list')

    user = get_object_or_404(User, id=user_id)
    new_role = get_object_or_404(Role, id=new_role_id)

    user.role = new_role

    user.save()

    with open('logs.log', 'a') as f:
        f.write(
            f"{datetime.now()} - {request.method} {request.path} Пользователь - {user.username} роль изменена на {user.role}\n")

    return redirect('admin-panel:user_list')


def system_settings(request):
    context = {}
    return render(request, 'admin-panel/system_settings_page.html', context=context)


def generate_username():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))


def create_user_view(request):
    if request.method == 'POST':
        username = generate_username()
        password = generate_password()
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')  # Получаем email
        role_id = request.POST.get('role')

        role = get_object_or_404(Role, id=role_id)
        user = User(username=username, first_name=first_name, last_name=last_name, email=email,
                    role=role)  # Добавляем email
        user.password = make_password(password)  # Хешируем пароль
        user.save()

        return render(request, 'admin-panel/user_created.html', {  # Возвращаем новый шаблон
            'username': username,
            'password': password,
            'email': email
        })

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password1'])
    #     if commit:
    #         user.save()
    #     email = EmailMessage(
    #         '',
    #         f'http://localhost:8000/verify/{user.id}',
    #         settings.EMAIL_HOST_USER,
    #         [self.cleaned_data['email']],
    #         headers={'Message-ID': 'foo'},
    #     )
    #     email.send()
    #     return user
    roles = Role.objects.all()
    return render(request, 'admin-panel/create_user.html', {'roles': roles})


def create_backup(request):
    os.system(f'python manage.py dumpdata > {settings.BASE_DIR}/backup.json')
    with open(f'{settings.BASE_DIR}\\backup.json', 'r', encoding='windows-1254') as file:
        response = HttpResponse(file.read(), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=backup.json'
        return response


def pg_backup(request):
    # os.system(f'python manage.py dumpdata > {settings.BASE_DIR}/backup.json')
    os.system(
        f'/Applications/pgAdmin\ 4.app/Contents/SharedSupport/pg_dump --file "{settings.BASE_DIR}/backups/backup-pg4-{datetime.now()}" --host "localhost" --port "5432" --username "postgres" --no-password --format=d --verbose "New"')
    # with open(f'{settings.BASE_DIR}\\backup.json', 'r', encoding='windows-1254') as file:
    #     response = HttpResponse(file.read(), content_type='application/json')
    #     response['Content-Disposition'] = 'attachment; filename=backup.json'
    #     return response
    return HttpResponse("резервная копия создана")


@csrf_exempt
def pg_recover(request):
    if request.method == 'POST':
        backup_dir = request.POST.get('backup_dir')

        if not os.path.isdir(backup_dir):
            return HttpResponse("Указанная директория не найдена.", status=400)

        backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.backup')]

        if not backup_files:
            return HttpResponse("Нет файлов бэкапа в указанной директории.", status=400)

        backup_file_path = os.path.join(backup_dir, backup_files[0])

        command = [
        '/Applications/pgAdmin 4.app/Contents/SharedSupport/pg_restore',
        '--host', 'localhost',
        '--port', '5432',
        '--username', 'postgres',
        '--no-password',
        '--dbname', 'TestBase',
        '--format', 'd',
        '--verbose',
        backup_file_path
        ]

        try:
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            return HttpResponse(f"Восстановление завершено: {result.stdout}")
        except subprocess.CalledProcessError as e:
            return HttpResponse(f"Ошибка восстановления: {e.stderr}", status=500)
        except Exception as e:
            return HttpResponse(f"Произошла ошибка: {str(e)}", status=500)

    return render(request, 'admin-panel/backup_form.html')


# def ExportDataToExcel(request):
#     objs = User.objects.all(), Role.objects.all(),
#     pd.DataFrame(objs).to_excel('out2put.xlsx')
#     return request
#     # return JsonResponse({
#     #     'status': 200
#     # })
#

def open_log_file(request):
    log_file_path = os.path.join(settings.BASE_DIR, 'logs.log')  # Используем BASE_DIR для указания корня проекта

    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            response = HttpResponse(log_file.read(), content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="logs.log"'
            return response
    else:
        return HttpResponse("Log file not found.", status=404)
