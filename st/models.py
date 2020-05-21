# -*- coding: utf-8 -*-
from datetime import date, datetime
from flask_security import RoleMixin, UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False, index=True)
    description = db.Column(db.String(256), nullable=True)


    def __repr__(self):
        return f'<Role {self.name}>'


    def __str__(self):
        return f'{self.name}'


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password = db.Column(db.String(256), nullable=False)
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship(
        'Role', secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )
    profile = db.relationship('Profile', uselist=False, backref='owner')
    visits = db.relationship('Visit', backref='user', lazy='dynamic')


    def __repr__(self):
        return f'<User email:{self.email}>'


    def __str__(self):
        return f'{self.email}'


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, index=True)
    birthdate = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(256), nullable=True, index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    def __repr__(self):
        return f'<Profile id:{self.id} name:{self.name}>'


    def __str__(self):
        return f'{self.name}'


    @property
    def age(self):
        return date.today() - self.birthdate


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True, unique=False)
    cost = db.Column(db.Float, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('service_types.id'))


    def __repr__(self):
        return f'<Service {self.id}>'


    def __str__(self):
        return f'{self.name}'


class ServiceType(db.Model):
    __tablename__ = 'service_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, unique=False, nullable=True)
    services = db.relationship('Service', backref='type', lazy='dynamic')


    def __repr__(self):
        return f'<ServiceType {self.id}>'


    def __str__(self):
        return f'{self.name}'


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False, index=True)
    chief_id = db.Column(db.Integer, db.ForeignKey('chiefs.id'))
    lessons = db.relationship('Lesson', backref='group', lazy='dynamic')


    def __repr__(self):
        return f'<Group {self.id}>'


    def __str__(self):
        return f'{self.name}'


class Chief(db.Model):
    __tablename__ = 'chiefs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False, index=True)
    type_id = db.Column(db.Integer, db.ForeignKey('chief_types.id'))
    groups = db.relationship('Group', backref='chief', lazy='dynamic')
    lessons = db.relationship('Lesson', backref='chief', lazy='dynamic')
    cost = db.Column(db.Float, nullable=False)


    def __repr__(self):
        return f'<Chief {self.id}>'


    def __str__(self):
        return f'{self.name}'


class ChiefType(db.Model):
    __tablename__ = 'chief_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, unique=False, nullable=True)
    chiefs = db.relationship('Chief', backref='type', lazy='dynamic')


    def __repr__(self):
        return f'<ChiefType {self.id}>'


    def __str__(self):
        return f'{self.name}'


class Gym(db.Model):
    __tablename__ = 'gyms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True, index=True)
    visits = db.relationship('Visit', backref='gym', lazy='dynamic')
    type_id = db.Column(db.Integer, db.ForeignKey('gym_types.id'))
    lessons = db.relationship('Lesson', backref='gym', lazy='dynamic')
    equipments = db.relationship('Equipment', backref='gym', lazy='dynamic')


    def __repr__(self):
        return f'<Gym {self.id}>'


    def __str__(self):
        return f'{self.name}'


class GymType(db.Model):
    __tablename__ = 'gym_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True, unique=False)
    gyms = db.relationship('Gym', backref='type', lazy='dynamic')


    def __repr__(self):
        return f'<GymType {self.id}>'


    def __str__(self):
        return f'{self.name}'


class Equipment(db.Model):
    __tablename__ = 'equipments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=False, index=True)
    description = db.Column(db.Text, nullable=True, unique=False)
    type_id = db.Column(db.Integer, db.ForeignKey('equipment_types.id'))
    gym_id = db.Column(db.Integer, db.ForeignKey('gyms.id'))


    def __repr__(self):
        return f'<Equipment {self.id}>'


    def __str__(self):
        return f'{self.name}'



class EquipmentType(db.Model):
    __tablename__ = 'equipment_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, unique=False, nullable=True)
    equipments = db.relationship('Equipment', backref='type', lazy='dynamic')


    def __repr__(self):
        return f'<EquipmentType {self.id}>'


    def __name__(self):
        return f'{self.name}'


class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True, unique=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('lesson_types.id'))
    chief_id = db.Column(db.Integer, db.ForeignKey('chiefs.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    gym_id = db.Column(db.Integer, db.ForeignKey('gyms.id'))


    def __repr__(self):
        return f'<Lesson {self.id}>'


    def __str__(self):
        return f'{self.name}'


class LessonType(db.Model):
    __tablename__ = 'lesson_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True, unique=False)
    lessons = db.relationship('Lesson', backref='type', lazy='dynamic')


    def __repr__(self):
        return f'<LessonType {self.id}>'


    def __str__(self):
        return f'{self.name}'


class Visit(db.Model):
    __tablename__ = 'visits'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    gym_id = db.Column(db.Integer, db.ForeignKey('gyms.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __repr__(self):
        return f'<Visit {self.id}>'


    def __str__(self):
        return f'{self.time} {self.user}'
