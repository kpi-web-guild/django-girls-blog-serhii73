"""Tests for models' Blog app."""

from datetime import datetime
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from ..models import Post


class PostModelTest(TestCase):
    """Tests for Post model."""

    def setUp(self):
        """Set up non-modifiable objects used by all test methods."""
        self.post = Post.objects.create(
            author=User.objects.create(username='bob'),
            title='Title',
            text='A few lines of text',
        )

    def tearDown(self):
        """Clean-up test data."""
        del self.post

    def test_title_label(self):
        """Test for title label."""
        field_label = self.post._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_text_label(self):
        """Test for text label."""
        field_label = self.post._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_created_date_label(self):
        """Test for created_date label."""
        field_label = self.post._meta.get_field('created_date').verbose_name
        self.assertEqual(field_label, 'created date')

    def test_published_date_label(self):
        """Test for published_date label."""
        field_label = self.post._meta.get_field('published_date').verbose_name
        self.assertEqual(field_label, 'published date')

    def test_str_method(self):
        """Test for __str__ method."""
        self.assertEqual('Title', self.post.__str__())

    @patch(
        'django.utils.timezone.now',
        lambda: datetime(
            day=11, month=9, year=2018, tzinfo=timezone.get_current_timezone()
        ),
    )
    def test_post_publish(self):
        """Test for publish method."""
        self.post.publish()
        self.assertEqual(
            self.post.published_date,
            datetime(
                day=11,
                month=9,
                year=2018,
                tzinfo=timezone.get_current_timezone(),
            ),
        )
