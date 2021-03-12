from unittest import TestCase, test
from seed import reset_db
import app

app.app.config['SQLALCHEMY_ECHO'] = False

reset_db()

class testUser(TestCase):

    def setUp(self):
        app.User.query.delete()
        new_user = app.User(first_name='bob', last_name='onion')
        app.db.session.add(new_user)
        app.db.session.commit()
        
        self.new_user = new_user

    def tearDown(self):
        app.User.query.delete()
        app.db.session.rollback()

    def test_setUp(self):
        """Test that setUp functions as expected"""
        with app.app.test_client() as client:
            res = client.get('/users')

            self.assertEqual(res.status_code, 200)
            self.assertIsInstance(self.new_user, app.User)
    
    def test_list_users(self):
        """Test status code and that user name is in the page"""
        with app.app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.new_user.full_name , html)

    def test_user_page(self):
        """Test status code and that user name is in the page."""
        with app.app.test_client() as client:
            res = client.get(f'/users/{self.new_user.id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.new_user.full_name , html)

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
        """ Edit new_user (bob onion) to Pak onion, should keep lastname and img-url if left empty"""
        with app.app.test_client() as client:
            data = {"first-name":"Pak", "last-name":"", "img-url":""}
            res = client.post(f'/users/{self.new_user.id}/edit', data=data , follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Pak onion', html)

    def test_delete_user(self):
        """Delete new user (bob onion) from db, check that status code is 200 and that a query returns an empty list"""
        with app.app.test_client() as client:
            res = client.get(f'users/{self.new_user.id}/delete', follow_redirects=True)
            users = app.User.query.all()
            self.assertEqual(res.status_code, 200)
            self.assertEqual(users, [])
    
class testPost(TestCase):

    @classmethod
    def setUpClass(self):
        user = app.User(first_name="Jus", last_name="Onion")
        app.db.session.add(user)
        app.db.session.commit()

        post = app.Post(title="new stuff", content="new stuff", user_id=user.id)
        app.db.session.add(post)
        app.db.session.commit()

        self.user_id = user.id
        self.post_id = post.id
        self.post_title = post.title

    @classmethod
    def tearDownClass(self):
        app.db.session.rollback()
        app.User.query.delete()
        app.Post.query.delete()

    def test_post_page(self):
        with app.app.test_client() as client:
            res = client.get(f'/posts/{self.post_id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.post_title, html)
    
    def test_update_post(self):
        with app.app.test_client() as client:
            data = {"post-title": "Knanye", "post-content": "LOREMIPSUM"}
            res = client.post(f'/posts/{self.post_id}/edit', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(data["post-title"], html)

    def test_delete_post(self):
        with app.app.test_client() as client:
            res = client.get(f'/posts/{self.post_id}/delete', follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertEqual([], app.Post.query.all())