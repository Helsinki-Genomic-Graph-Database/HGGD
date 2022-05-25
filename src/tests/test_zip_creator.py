from imghdr import tests
import unittest
import os
import shutil
from src.zip_creator import zipcreator_service

class TestZipReader(unittest.TestCase):
    def setUp(self):
        self.directory = "src/tests/testdata"

    def test_create_zip_no_testfolder(self):
        self.delete_zip_folder(self.directory)
        zipfile = zipcreator_service.create_zip("zip1", self.directory)
        self.assertEqual("zip1.zip", zipfile)

    def test_create_zip_testfolder_exists_no_zip_file(self):
        self.make_zip_folder(self.directory)
        zipfile = zipcreator_service.create_zip("zip2", self.directory)
        self.assertEqual("zip2.zip", zipfile)

    def test_create_zip_testfolder_exists_zip_file_exists(self):
        self.delete_zip_folder(self.directory)
        self.make_zip_folder(self.directory)
        self.make_zip_file("zip3", self.directory)
        zipfile = zipcreator_service.create_zip("zip4", self.directory)
        self.assertEqual("zip3.zip", zipfile)

    def delete_zip_folder(self, directory):
        if os.path.exists(f"{directory}/zip"):
            shutil.rmtree(f"{directory}/zip")

    def make_zip_folder(self, directory):
        os.mkdir(f"{directory}/zip")

    def make_zip_file(self, filename, directory):
        shutil.make_archive(f"{directory}/zip/{filename}", 'zip', directory)
