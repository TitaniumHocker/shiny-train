# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, abort
from flask_security import auth_required, current_user
from st.blueprints.public import public


@public.route('/')
def index():
    return render_template('public/index.html', page_title='Главная')


@public.route('/profile/<int:id>', methods=['GET', 'POST'])
@auth_required()
def profile(id):
    if request.method == 'GET':
        return render_template('public/profile.html')


@public.route('/chats', methods=['GET', 'POST'])
@auth_required()
def chats():
    return render_template('public/chats.html')


@public.route('/friends', methods=['GET', 'POST'])
@auth_required()
def friends():
    return render_template('public/friends.html')
