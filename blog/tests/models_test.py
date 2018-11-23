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

    def test_right_title(self):
        """Test right title output."""
        assert str(self.post) == 'Title'

    @patch(
        'django.utils.timezone.now',
        lambda: datetime(
            day=11, month=9, year=2018, tzinfo=timezone.get_current_timezone()
        ),
    )
    def test_post_publish(self):
        """Test for publish method."""
        self.post.publish()
        assert self.post.published_date == datetime(
            day=11, month=9, year=2018, tzinfo=timezone.get_current_timezone()
        )
