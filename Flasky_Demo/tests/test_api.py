# __Time__ : 2020/10/14 下午4:56
# __Author__ : '__YDongY__'


# import unittest
# import json
# import re
# from base64 import b64encode
# from flask import url_for
# from app import create_app, db
# from app.models import User
#
#
# class APITestCase(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app('testing')
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         # db.create_all()
#         self.client = self.app.test_client()
#
#     def tearDown(self):
#         # db.session.remove()
#         # db.drop_all()
#         self.app_context.pop()
#
#     def get_api_headers(self, username, password):
#         return {
#             'Authorization': 'Basic ' + b64encode(
#                 (username + ':' + password).encode('utf-8')).decode('utf-8'),
#             'Accept': 'application/json',
#             'Content-Type': 'application/json'
#         }
#
#     def test_404(self):
#         response = self.client.get(
#             '/wrong/url',
#             headers=self.get_api_headers('email', 'password'))
#         self.assertTrue(response.status_code == 404)
#         json_response = json.loads(response.data.decode('utf-8'))
#         self.assertTrue(json_response['error'] == 'not found')
#
#     def test_no_auth(self):
#         response = self.client.get(url_for('api.get_posts'),
#                                    content_type='application/json')
#         self.assertTrue(response.status_code == 200)
#
#     def test_users(self):
#         add two users
#         r = Role.query.filter_by(name='User').first()
#         self.assertIsNotNone(r)
#         u1 = User(email='john@example.com', username='john',
#                   password='cat', confirmed=True, role=r)
#         u2 = User(email='susan@example.com', username='susan',
#                   password='dog', confirmed=True, role=r)
#         db.session.add_all([u1, u2])
#         db.session.commit()
#
#         get users
#         response = self.client.get(
#             url_for('api.get_user', id=u1.id),
#             headers=self.get_api_headers('susan@example.com', 'dog'))
#         self.assertTrue(response.status_code == 200)
#         json_response = json.loads(response.data.decode('utf-8'))
#         self.assertTrue(json_response['username'] == 'john')
#         response = self.client.get(
#             url_for('api.get_user', id=u2.id),
#             headers=self.get_api_headers('susan@example.com', 'dog'))
#         self.assertTrue(response.status_code == 200)
#         json_response = json.loads(response.data.decode('utf-8'))
#         self.assertTrue(json_response['username'] == 'susan')
