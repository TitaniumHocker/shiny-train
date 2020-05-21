# -*- coding: utf-8 -*-
import os
from flask import abort, url_for, request, redirect
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_security import current_user
from st.models import db, User, Role, Profile


class SecureAdminMixin():
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_calstack(self, name, **kwargs):
        if current_user.is_authenticated:
            return abort(403)
        return redirect(url_for('security.login', next=request.url))


class AdminModelView(SecureAdminMixin, ModelView): pass


class SecureStaffMixin(SecureAdminMixin):
    def is_accessible(self):
        return current_user.has_role('staff') or current_user.has_role('admin')


class SecureIndex(SecureStaffMixin, AdminIndexView): pass
class StaffModelView(SecureStaffMixin, ModelView): pass
class SecureFileAdmin(SecureStaffMixin, FileAdmin): pass


class RoleView(AdminModelView):
    column_labels = {
        'name': 'Имя',
        'description': 'Описание'
    }


class UserView(AdminModelView):
    column_exclude_list = ('password', 'messages', 'chats')
    column_searchable_list = ('email',)
    column_editable_list = ('active',)
    column_labels = {
        'username': 'Имя пользователя',
        'friends': 'Друзья',
        'email': 'Почтовый адрес',
        'active': 'Активирован',
        'password': 'Пароль',
        'roles': 'Роли',
        'confirmed_at': 'Подтвержден',
        'profile': 'Профиль',
    }
    form_excluded_columns = ('messages', 'chats', 'profile')


class ProfileView(StaffModelView):
    column_searchable_list = ('name', 'address')
    column_labels = {
        'name': 'Имя',
        'birthdate': 'Дата рождения',
        'address': 'Адрес'
    }


admin = Admin(
    name='LB', template_mode='bootstrap2',
    index_view=SecureIndex(name='Админка')
)
admin.add_link(MenuLink(name='На главную', url='/'))
admin.add_link(MenuLink(name='Выход', url='/logout'))

path = os.path.join(os.path.dirname(__file__), 'static')
admin.add_view(SecureFileAdmin(path, '/static/', name='Файлы'))

admin.add_view(UserView(User, db.session, name='Пользователи'))
admin.add_view(RoleView(Role, db.session, name='Роли'))
admin.add_view(ProfileView(Profile, db.session, name='Профили'))
