from unittest import TestCase, test
import app

app.app.config['SQLALCHEMY_ECHO'] = False

app.db.drop_all()
app.db.create_all()

class test_blogly(TestCase):

    def setUp(self):
        newUser = app.User(first_name='bob', last_name='onion')
        app.db.session.add(newUser)
        app.db.session.commit()
        
        self.newUser = newUser

    def tearDown(self):
        app.User.query.delete()

    def test_setUp(self):
        """Test that setup functions as expected"""
        with app.app.test_client() as client:
            res = client.get('/users')

            self.assertEqual(res.status_code, 200)
            self.assertIsInstance(self.newUser, app.User)
            self.assertEqual(str(self.newUser), '<User 1 bob onion>')
    
    def test_list_users(self):
        """Test status code and that user name is in the page"""
        with app.app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.newUser.full_name , html)

    def test_user_page(self):
        """Test status code and that user name is in the page."""
        with app.app.test_client() as client:
            res = client.get(f'/users/{self.newUser.id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.newUser.full_name , html)

    def test_create_user(self):
        """Create a new user and test that status code is 200 
        and that in the list users page the new user's name appears"""
        with app.app.test_client() as client:
            data = {"first-name": "Pepper", "last-name":"peepper", "img-url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/220px-Image_created_with_a_mobile_phone.png"}
            res = client.post('/users/new', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Pepper peepper", html)

    def test_edit_user(self):
        """ Edit newUser (bob onion) to Pak onion, should keep lastname and img-url if left empty"""
        with app.app.test_client() as client:
            data = {"first-name":"Pak", "last-name":"", "img-url":""}
            res = client.post(f'/users/{self.newUser.id}/edit', data=data , follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Pak onion', html)

    def test_delete_user(self):
        """Delete new user (bob onion) from db, check that status code is 200 and that a query returns an empty list"""
        with app.app.test_client() as client:
            res = client.get(f'users/{self.newUser.id}/delete', follow_redirects=True)
            users = app.User.query.all()
            self.assertEqual(res.status_code, 200)
            self.assertEqual(users, [])
            