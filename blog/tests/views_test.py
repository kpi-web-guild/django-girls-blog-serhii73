"""Test for views."""

from datetime import datetime
from unittest.mock import patch

from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from ..models import Post


class PostListTest(TestCase):
    """Tests for Post views."""

    def setUp(self):
        """Set up non-modifiable objects used by all test methods."""
        self.time_z = timezone.get_current_timezone()
        self.client = Client()
        self.user = User.objects.create_superuser(
            username='bob', password='password', email='email@email.com'
        )
        self.test_user2 = User.objects.create_user(
            username='testuser2', password='12345'
        )

        self.post_first = Post.objects.create(
            author=self.user,
            title='Title post first',
            text='Text post first',
            published_date=datetime(
                day=8, month=11, year=2018, tzinfo=self.time_z
            ),
        )

        self.post_second = Post.objects.create(
            author=self.user,
            title='Title post second',
            text='Text post second',
            published_date=datetime(
                day=8, month=11, year=2016, tzinfo=self.time_z
            ),
        )

        self.post_third = Post.objects.create(
            author=self.user,
            title='Title post third',
            text='Text post third',
            published_date=datetime(
                day=8, month=11, year=2014, tzinfo=self.time_z
            ),
        )

    def tearDown(self):
        """Clean-up test data."""
        del self.time_z
        del self.client
        del self.user
        del self.test_user2

        del self.post_first
        del self.post_second
        del self.post_third

    def test_logged_correct_temp(self):
        """The user is logged in and used the correct template."""
        self.client.login(username='bob', password='password')
        resp = self.client.get(reverse('post_list'))

        self.assertEqual(str(resp.context['user']), 'bob')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/post_list.html')

    def test_post_list_correct_order(self):
        """Test show post list on the page and test correct order."""
        with patch(
            'django.utils.timezone.now',
            lambda: datetime(day=1, month=1, year=2018, tzinfo=self.time_z),
        ):
            self.client.login(username='bob', password='password')
            resp = self.client.get(reverse('post_list'))
            posts = resp.context['posts']

            assert posts.first().title == 'Title post second'
            assert posts.first().text == 'Text post second'
            assert posts.first().published_date, datetime(
                day=8, month=11, year=2016, tzinfo=self.time_z
            )

            assert posts.last().title == 'Title post third'
            assert posts.last().text == 'Text post third'
            assert posts.last().published_date, datetime(
                day=8, month=11, year=2014, tzinfo=self.time_z
            )

            soup = BeautifulSoup(str(resp.content), 'html.parser')
            posts = [
                i.text.replace('\\n', '').strip() for i in soup.find_all('h1')
            ][1:]
            assert posts == ['Title post second', 'Title post third']

            self.assertTemplateUsed(
                resp, 'blog/post_list.html', 'blog/base.html'
            )

    def test_post_detail(self):
        """Test post contents displayed correctly."""
        resp = self.client.get(reverse('post_detail', kwargs={'pk': 1}))
        assert resp.status_code == 200

        self.assertTemplateUsed(
            resp, 'blog/post_detail.html', 'blog/base.html'
        )

        title_detail_page = resp.context['post'].title
        assert title_detail_page == 'Title post first'

        text_detail_page = resp.context['post'].text
        assert text_detail_page == 'Text post first'

    def test_post_detail_not_exist_post(self):
        """Test if the post does not exist."""
        resp = self.client.get(reverse('post_detail', kwargs={'pk': 11}))
        self.assertEqual(404, resp.status_code)

    def test_post_new_anonymous_user(self):
        """Test create post, anonymousUser."""
        resp = self.client.get(reverse('post_new'))
        assert resp.status_code == 200

        with self.assertRaises(Exception) as context:
            self.client.post(
                reverse('post_new'),
                {
                    'author': 'paul',
                    'title': 'Post with post new',
                    'text': 'Text with post new',
                },
                follow=True,
            )

        assert '"Post.author" must be a "User"' in str(context.exception)
        self.assertTemplateUsed(resp, 'blog/post_edit.html', 'blog/base.html')

    def test_post_new_and_edit(self):
        """Test create and edit post."""
        self.client.login(username='testuser2', password='12345')

        resp = self.client.post(
            reverse('post_new'),
            {
                'author': 'testuser2',
                'title': 'Post with post new',
                'text': 'Text with post new',
            },
            follow=True,
        )
        assert resp.status_code == 200

        self.assertTemplateUsed(
            resp, 'blog/post_detail.html', 'blog/base.html'
        )

        title_new_on_the_page = resp.context['post'].title
        assert title_new_on_the_page == 'Post with post new'

        text_new_on_the_page = resp.context['post'].text
        assert text_new_on_the_page == 'Text with post new'

        resp = self.client.post(
            reverse('post_edit', kwargs={'pk': 4}),
            {
                'author': 'testuser2',
                'title': 'Post with post edit',
                'text': 'Text with post edit',
            },
            follow=True,
        )

        title_edit_on_the_page = resp.context['post'].title
        assert title_edit_on_the_page == 'Post with post edit'

        resp = self.client.get(reverse('post_edit', kwargs={'pk': 1}))
        assert resp.status_code == 200
