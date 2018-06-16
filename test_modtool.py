""" The file for testing the gr-modtool scripts """
import shutil
import tempfile
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
            args = {'module_name':'howto', 'directory': self.test_dir}
            ModToolNewModule(**args).run()
        except (TypeError, ModToolException):
            self.f_newmod = True
        else:
            try:
                args = {'blockname':'square_ff', 'block_type':'general',
                        'lang':'cpp', 'directory': self.test_dir + '/gr-howto',
                        'add_python_qa': True}
                ModToolAdd(**args).run()
            except (TypeError, ModToolException):
                self.f_add = True

    def tearDown(self):
        """ removes the created module """
        # Required, else the new-module directory command
        # in setup with throw exception after first test
        ## cannot remove if directory is not created
        if not self.f_newmod:
            rmdir = self.test_dir + '/gr-howto'
            shutil.rmtree(rmdir)

    def test_newmod(self):
        """ Tests for the API function newmod """
        ## Tests for proper exceptions ##
        test_dict = {}
        test_dict['directory'] = self.test_dir
        # module name not specified
        self.assertRaises(TypeError, ModToolNewModule, **test_dict)
        self.assertRaises(TypeError, ModToolNewModule, 'a'=='a')
        self.assertRaises(TypeError, ModToolNewModule, )
        test_dict['module_name'] = 'howto'
        # expected module_name as a string instead of dict
        self.assertRaises(TypeError, ModToolNewModule, test_dict)
        # directory already exists
        # will not be raised if the command in setup failed
        self.assertRaises(ModToolException, ModToolNewModule, **test_dict)

        ## Some tests for checking the created directory, sub-directories and files ##
        test_dict['module_name'] = 'test'
        ModToolNewModule(**test_dict).run()
        self.assertTrue(path.isdir(self.test_dir+'/gr-test'))
        self.assertTrue(path.isdir(self.test_dir+'/gr-test/lib'))
        self.assertTrue(path.exists(self.test_dir+'/gr-test/CMakeLists.txt'))

    def test_add(self):
        """ Tests for the API function add """
        ## skip tests if newmod command wasn't successful
        if self.f_newmod:
            raise unittest.SkipTest("setUp for API function 'add' failed")

        ## Tests for proper exceptions ##
        self.assertRaises(TypeError, ModToolAdd, )
        test_dict = {}
        test_dict['directory'] = self.test_dir + '/gr-howto'
        # missing 3 positional arguments blockname, block_type, lang
        self.assertRaises(TypeError, ModToolAdd, **test_dict)
        test_dict['blockname'] = 'add_ff'
        # missing 2 positional arguments block_type, lang
        self.assertRaises(TypeError, ModToolAdd, **test_dict)
        test_dict['block_type'] = 'general'
        # missing positional argument lang
        self.assertRaises(TypeError, ModToolAdd, **test_dict)
        test_dict['lang'] = 'cxx'
        # incorrect language
        self.assertRaises(ModToolException, ModToolAdd, **test_dict)
        test_dict['lang'] = 'cpp'
        test_dict['add_cpp_qa'] = 'Wrong'
        # boolean is expected for add_cpp_qa
        self.assertRaises(ModToolException, ModToolAdd, **test_dict)
        test_dict['add_cpp_qa'] = True
        test_dict['block_type'] = 'generaleee'
        # incorrect block type
        self.assertRaises(ModToolException, ModToolAdd, **test_dict)
        test_dict['block_type'] = 'general'
        test_dict['skip_lib'] = 'fail'
        # boolean value is expected for skip_lib
        self.assertRaises(ModToolException, ModToolAdd, **test_dict)
        test_dict['skip_lib'] = True
        # missing relevant subdir
        self.assertRaises(ModToolException, ModToolAdd, **test_dict)

        ## Some tests for checking the created directory, sub-directories and files ##
        test_dict['skip_lib'] = False
        ModToolAdd(**test_dict).run()
        self.assertTrue(path.isdir(self.test_dir+'/gr-howto/python'))
        self.assertTrue(path.isdir(self.test_dir+'/gr-howto/include'))
        self.assertTrue(path.isdir(self.test_dir+'/gr-howto/docs'))
        self.assertTrue(path.isdir(self.test_dir+'/gr-howto/cmake'))
        self.assertTrue(path.exists(self.test_dir+'/gr-howto/CMakeLists.txt'))
        self.assertTrue(path.exists(self.test_dir+'/gr-howto/lib/qa_add_ff.cc'))
        self.assertTrue(path.exists(self.test_dir+'/gr-howto/lib/add_ff_impl.cc'))
        self.assertTrue(path.exists(self.test_dir+'/gr-howto/grc/howto_add_ff.xml'))

    def test_rename(self):
        """ Tests for the API function rename """
        if self.f_newmod or self.f_add:
            raise unittest.SkipTest("setUp for API function 'rename' failed")

        self.assertRaises(TypeError, ModToolRename, )
        test_dict = {}
        test_dict['directory'] = self.test_dir+'/gr-howto'
        # Missing 2 positional arguments blockname, new_name
        self.assertRaises(TypeError, ModToolRename, **test_dict)
        test_dict['blockname'] = 'square_ff'
        # Missing 1 positional argument new_name
        self.assertRaises(TypeError, ModToolRename, **test_dict)
        test_dict['new_name'] = '//#'
        # Invalid new block name!
        self.assertRaises(ModToolException, ModToolRename, **test_dict)
        test_dict['new_name'] = None
        # New Block name not specified
        self.assertRaises(ModToolException, ModToolRename, **test_dict)

        ## Some tests for checking the renamed files ##
        test_dict['new_name'] = 'div_ff'
        ModToolRename(**test_dict).run()
        self.assertTrue(path.exists(self.test_dir+'/gr-howto/lib/div_ff_impl.h'))
        self.assertTrue(path.exists(self.test_dir+'/gr-howto/lib/div_ff_impl.cc'))
        self.assertTrue(path.exists(self.test_dir+'/gr-howto/python/qa_div_ff.py'))
        self.assertTrue(path.exists(self.test_dir+'/gr-howto/grc/howto_div_ff.xml'))

    def test_remove(self):
        """ Tests for the API function remove """
        if self.f_newmod or self.f_add:
            raise unittest.SkipTest("setUp for API function 'remove' failed")

        self.assertRaises(TypeError, ModToolRename, )
        test_dict = {}
        # missing positional argument blockname
        self.assertRaises(TypeError, ModToolRename, **test_dict)
        test_dict['directory'] = self.test_dir+'/gr-howto'
        self.assertRaises(TypeError, ModToolRename, **test_dict)

        ## Some tests to check blocks are not removed with different blocknames ##
        test_dict['blockname'] = 'div_ff'
        ModToolRemove(**test_dict).run()
        self.assertTrue(path.exists(self.test_dir+'/gr-howto/lib/square_ff_impl.h'))
        self.assertTrue(path.exists(self.test_dir+'/gr-howto/lib/square_ff_impl.cc'))
        self.assertTrue(path.exists(self.test_dir+'/gr-howto/python/qa_square_ff.py'))
        self.assertTrue(path.exists(self.test_dir+'/gr-howto/grc/howto_square_ff.xml'))

        ## Some tests for checking the non-existence of removed files ##
        test_dict['blockname'] = 'square_ff'
        ModToolRemove(**test_dict).run()
        self.assertTrue(not path.exists(self.test_dir+'/gr-howto/lib/square_ff_impl.h'))
        self.assertTrue(not path.exists(self.test_dir+'/gr-howto/lib/square_ff_impl.cc'))
        self.assertTrue(not path.exists(self.test_dir+'/gr-howto/python/qa_square_ff.py'))
        self.assertTrue(not path.exists(self.test_dir+'/gr-howto/grc/howto_square_ff.xml'))
