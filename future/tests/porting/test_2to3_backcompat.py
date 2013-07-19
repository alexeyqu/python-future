"""
This module contains tests for whether the output of 2to3 can be run
immediately under Python with the future module using:

    from future import *

"""

from __future__ import print_function, absolute_import

import unittest
import textwrap
from subprocess import Popen, PIPE, check_output


class Test2to3Simple(unittest.TestCase):
    def test_range_slice(self):
        code = '''
        from future.features import range
        for i in range(10**11)[:10]:
            pass
        '''
        self.simple_convert_and_check(code)

    def test_super(self):
        code = '''
        from future.features import super
        class VerboseList(list):
            def append(self, item):
                print 'Adding an item'
                super(VerboseList, self).append(item)
        '''
        self.simple_convert_and_check(code)

    def test_apply(self):
        code = '''
        from future import disable_obsolete_builtins
        def addup(*x):
            return sum(x)
        
        assert apply(addup, (10,20)) == 30
        '''
        self.simple_convert_and_check(code, fixers=['apply'])
    
    def test_renamed_modules(self):
        code = '''
        import ConfigParser
        import copy_reg
        import cPickle
        import cStringIO
        '''
        self.simple_convert_and_check(code, fixers=['imports'])
    
    def simple_convert_and_check(self, code, fixers=['all']):
        """
        Tests a complete conversion of this simple piece of code from the docs
        here:
            http://docs.python.org/2/library/2to3.html
        and whether 2to3 can be applied and then the resulting code be
        automatically run under Python 2 with the future module.
        """
        with open('mytestscript.py', 'w') as f:
            f.write('from __future__ import print_function, absolute_import\n')
            # f.write('from future import *\n')
            f.write(textwrap.dedent(code))
        output = check_output(['2to3', 'mytestscript.py', '-x', 'future', '-w'])
        # print(output)
        output2 = check_output(['python2', 'mytestscript.py'])
        # print(output2)

    def test_raw_input(self, interpreter='python2'):
        """
        Passes in a string to the waiting input()
        """
        code = '''
        from future import *
        def greet(name):
            print "Hello, {0}!".format(name)
        print "What's your name?"
        name = raw_input()
        greet(name)
        '''
        with open('mytestscript.py', 'w') as f:
            f.write(textwrap.dedent(code))
        output = check_output(['2to3', 'mytestscript.py', '-x', 'future', '-w'])
        print(output)
        p1 = Popen([interpreter, 'mytestscript.py'], stdout=PIPE, stdin=PIPE)
        (stdout, stderr) = p1.communicate('Ed')
        print(stdout)
        print(stderr)
        self.assertEqual(stdout, "What's your name?\nHello, Ed!\n")

        
unittest.main(failfast=True)
