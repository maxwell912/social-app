from django.test import TestCase

from .factories import FileFactory


class FilesTestCase(TestCase):

    @classmethod
    def setUp(cls):
        """Create new factory file."""
        cls.file = FileFactory()

    def test_file_path(self):
        """Check exists file's path."""
        self.assertTrue(hasattr(self.file, 'path'))
