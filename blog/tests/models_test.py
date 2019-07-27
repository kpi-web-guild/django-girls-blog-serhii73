"""Tests for models."""

from datetime import datetime
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from ..models import Post


class PostModelTest(TestCase):
    """Tests for post model."""

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

    def test_post_str(self):
        """Test post stringification."""
        assert str(self.post) == 'Title'

    @patch(
        'django.utils.timezone.now',
        lambda: datetime(
            day=11, month=9, year=2018, tzinfo=timezone.get_current_timezone()
        ),
    )
    def test_post_publish(self):
        """Test post has a published date after publish method called."""
        assert self.post.published_date is None

        assert self.post.published_date is None
        self.post.publish()

        assert self.post.published_date == datetime(
            day=11, month=9, year=2018, tzinfo=timezone.get_current_timezone()
        )
