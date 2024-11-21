from admin_panel.views import UserListView, block_user_view, change_user_role, system_settings, create_user_view, \
    unblock_user_view, pg_backup, open_log_file, pg_recover
from django.urls import path, include
app_name = 'admin_panel'


urlpatterns = [
    # path('', views.adminHome, name='home'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('block_user/<int:user_id>/', block_user_view, name='block_user'),
    path('unblock_user/<int:user_id>/', unblock_user_view, name='unblock_user'),
    path('users/change-role/', change_user_role, name='change_user_role'),
    path('settings/', system_settings, name='system_settings'),
    path('create_user/', create_user_view, name='create_user'),

    path('backup/', pg_backup, name='backup'),
    path('recoverbackup/', pg_recover, name='recoverbackup'),
    # path('export/', ExportDataToExcel, name='export_to_excel'),
    path('open-log/', open_log_file, name='open_log_file'),

]
