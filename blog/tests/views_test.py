"""Tests for views' Blog app."""

from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from ..models import Post


class PostListTest(TestCase):
    """Tests for Post views."""

    def setUp(self):
        """Set up non-modifiable objects used by all test methods."""
        bob = User.objects.create(username='bob')
        self.post_first = Post.objects.create(
            author=bob,
            title='Title Bob',
            text='Text bob',
            published_date=datetime(day=8, month=11, year=2018),
        )

        john = User.objects.create(username='john')

        self.post_second = Post.objects.create(
            author=john, title='Title John', text='Text John'
        )
        self.post_third = Post.objects.create(
            author=john, title='Title John 2', text='Text John 2'
        )
        self.post_third.publish()

    def tearDown(self):
        """Clean-up test data."""
        del self.post_first
        del self.post_second
        del self.post_third

    def test_post_list(self):
        """Test show post list on the page."""
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response, 'blog/post_list.html', 'blog/base.html'
        )
        self.assertEqual(len(response.context['posts']), 2)

    def test_post_detail(self):
        """Test post detail."""
        response = self.client.get(reverse('post_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response, 'blog/post_detail.html', 'blog/base.html'
        )

        self.assertIn(b'Title Bob', response.content)
        self.assertIn(b'Text bob', response.content)

        self.assertEqual(str(response.context['post']), 'Title Bob')

    def test_post_new_and_edit(self):
        """Test create and edit post."""
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 200)

        paul_password = 'test'
        paul = User.objects.create_superuser(
            username='paul', password=paul_password, email='e@e.com'
        )
        self.client.login(username=paul.username, password=paul_password)

        response = self.client.post(
            reverse('post_new'),
            {
                'author': paul,
                'title': 'Post with post new',
                'text': 'Text with post new',
            },
            follow=True,
        )
        self.assertEqual(200, response.status_code)

        self.assertTemplateUsed(
            response, 'blog/post_detail.html', 'blog/base.html'
        )

        self.assertIn(b'Post with post new', response.content)
        self.assertIn(b'Text with post new', response.content)

        response = self.client.post(
            reverse('post_edit', kwargs={'pk': 1}),
            {
                'author': paul,
                'title': 'Post with post edit',
                'text': 'Text with post edit',
            },
            follow=True,
        )

        self.assertIn(b'Post with post edit', response.content)
        self.assertIn(b'Text with post edit', response.content)

        response = self.client.get(reverse('post_edit', kwargs={'pk': 1}))
        assert response.status_code == 200
