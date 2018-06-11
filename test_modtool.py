import shutil, tempfile
from os import path
import unittest
from gnuradio.modtool.core import *

class TestModToolCore(unittest.TestCase):
	""" The tests for the modtool core """

	@classmethod
	def setUpClass(cls):
		""" create a temporary directory """
		cls.test_dir = tempfile.mkdtemp()

	@classmethod
	def tearDownClass(cls):
		""" remove the directory after the test """
		shutil.rmtree(cls.test_dir)

	def setup(self):
		""" create a new module and block before every test """
		ModToolNewModule().run({'module_name':'howto', 'directory': cls.test_dir})
		ModToolAdd().run({'blockname':'square_ff', 'block_type':'general', 'language':'cpp', 'directory': cls.test_dir + '/gr-howto'})
		
	def test_newmod(self):
		pass

	def test_add(self):
		pass	
		
	def test_rename(self):
		pass

	def test_rm(self):
		pass
