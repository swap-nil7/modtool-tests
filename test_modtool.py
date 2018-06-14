import shutil, tempfile
from os import path
import unittest
import warnings

from gnuradio.modtool.core import * 

class TestModToolCore(unittest.TestCase):
	""" The tests for the modtool core """

	def __init__(self, *args, **kwargs):
		super(TestModToolCore, self).__init__(*args, **kwargs)
		self.f_add = False
		self.f_newmod = False

	@classmethod
	def setUpClass(cls):
		""" create a temporary directory """
		cls.test_dir = tempfile.mkdtemp()

	@classmethod
	def tearDownClass(cls):
		""" remove the directory after the test """
		shutil.rmtree(cls.test_dir)

	def setUp(self):
		""" create a new module and block before every test """
		try:
			warnings.simplefilter("ignore", ResourceWarning)
			ModToolNewModule({'module_name':'howto', 'directory': self.test_dir}).run()
		except ModToolException:
			self.f_newmod = True
		else:
			try:
				args = {'blockname':'square_ff', 'block_type':'general', 
					    'lang':'cpp', 'directory': self.test_dir + '/gr-howto'}
				ModToolAdd(args).run()
			except ModToolException:
				self.f_add = True

	def tearDown(self):
		""" removes the created module """
		# we cannot remove this, else the new-module directory command in setup with throw exception
		rmdir = self.test_dir + '/gr-howto'
		shutil.rmtree(rmdir)

	def test_newmod(self):
		""" Tests for the API function newmod """
		## Tests for proper exceptions ##
		self.assertRaises(AttributeError, ModToolNewModule, 'a', 'b')
		self.assertRaises(AttributeError, ModToolNewModule, 'a')
		self.assertRaises(ModToolException, ModToolNewModule, )
		self.assertRaises(ModToolException, ModToolNewModule, module_name='fail')
		self.assertRaises(ModToolException, ModToolNewModule, {})
		self.assertRaises(ModToolException, ModToolNewModule, {'module_name':'howto', 'directory': self.test_dir})

		## Some tests for checking the created directory, sub-directories and files ## 
		ModToolNewModule({'module_name': 'test', 'directory': self.test_dir}).run()
		self.assertTrue(path.isdir(self.test_dir+'/gr-test'))
		self.assertTrue(path.isdir(self.test_dir+'/gr-test/lib'))
		self.assertTrue(path.exists(self.test_dir+'/gr-test/CMakeLists.txt'))

	def test_add(self):
		""" Tests for the API function add """
		if self.f_newmod:
			raise unittest.SkipTest("setUp for API function 'add' failed")

		## Tests for proper exceptions ##
		#self.assertRaises(TypeError, ModToolAdd().run, )
		test_dict = {}
		test_dict['directory'] = self.test_dir + '/gr-howto'
		self.assertRaises(ModToolException, ModToolAdd, test_dict)
		test_dict['blockname'] = 'add_ff'
		self.assertRaises(ModToolException, ModToolAdd, test_dict)
		test_dict['block_type'] = 'general'
		self.assertRaises(ModToolException, ModToolAdd, test_dict)
		test_dict['lang'] = 'cxx'
		self.assertRaises(ModToolException, ModToolAdd, test_dict)
		test_dict['lang'] = 'cpp'
		test_dict['add_cpp_qa'] = 'Wrong'
		self.assertRaises(ModToolException, ModToolAdd, test_dict)
		test_dict['add_cpp_qa'] = True
		test_dict['block_type'] = 'generaleee'
		self.assertRaises(ModToolException, ModToolAdd, test_dict)
		test_dict['block_type'] = 'general'
		test_dict['skip_lib'] = 'fail'
		self.assertRaises(ModToolException, ModToolAdd, test_dict)
		test_dict['skip_lib'] = True
		self.assertRaises(ModToolException, ModToolAdd, test_dict)
		test_dict['skip_lib'] = False

		## Some tests for checking the created directory, sub-directories and files ##
		ModToolAdd(test_dict).run()
		self.assertTrue(path.exists(self.test_dir+'/gr-howto/lib/qa_add_ff.cc'))
		self.assertTrue(path.exists(self.test_dir+'/gr-howto/lib/add_ff_impl.cc'))


	def test_rename(self):
		""" Tests for the API function rename """
		if self.f_newmod or self.f_add:
			raise unittest.SkipTest("setUp for API function 'rename' failed")
		pass

	def test_remove(self):
		""" Tests for the API function remove """
		if self.f_newmod or self.f_add:
			raise unittest.SkipTest("setUp for API function 'remove' failed")

		test_dict = {}
		test_dict['blockname'] = 'square_ff'
		test_dict['directory'] = self.test_dir+'/gr-howto'
		ModToolRemove(test_dict).run()