##
# Copyright 2013 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""Unit tests for eb command line options.

@author: Kenneth Hoste (Ghent University)
"""

import os
import re
import tempfile
from unittest import TestCase, TestLoader
from unittest import main as unittestmain

from easybuild.main import main
from easybuild.tools.build_log import init_logger
from easybuild.tools.options import EasyBuildOptions

class CommandLineOptionsTest(TestCase):
    """Testcases for command line options."""

    def setUp(self):
        """Prepare for running unit tests."""
        pass

    def tearDown(self):
        """Post-test cleanup."""
        pass

    def test_help_short(self, txt=None):
        """Test short help message."""

        if txt is None:
            topt = EasyBuildOptions(
                                    go_args=['-h'],
                                    go_nosystemexit=True,  # when printing help, optparse ends with sys.exit
                                    go_columns=100,  # fix col size for reproducible unittest output
                                    help_to_string=True,  # don't print to stdout, but to StingIO fh,
                                    prog='easybuildoptions_test',  # generate as if called from generaloption.py
                                   )

            outtxt = topt.parser.help_to_file.getvalue()
        else:
            outtxt = txt

        self.assertTrue(re.search(' -h ', outtxt), "Only short options included in short help")
        self.assertTrue(re.search("show short help message and exit", outtxt), "Documentation included in short help")
        self.assertEqual(re.search("--short-help ", outtxt), None, "Long options not included in short help")
        self.assertEqual(re.search("Software search and build options", outtxt), None, "Not all option groups included in short help (1)")
        self.assertEqual(re.search("Regression test options", outtxt), None, "Not all option groups included in short help (2)")

    def test_help_long(self):
        """Test long help message."""

        topt = EasyBuildOptions(
                                go_args=['-H'],
                                go_nosystemexit=True,  # when printing help, optparse ends with sys.exit
                                go_columns=100,  # fix col size for reproducible unittest output
                                help_to_string=True,  # don't print to stdout, but to StingIO fh,
                                prog='easybuildoptions_test',  # generate as if called from generaloption.py
                               )
        outtxt = topt.parser.help_to_file.getvalue()

        self.assertTrue(re.search("-H, --help", outtxt), "Long documentation expanded in long help")
        self.assertTrue(re.search("show short help message and exit", outtxt), "Documentation included in long help")
        self.assertTrue(re.search("Software search and build options", outtxt), "Not all option groups included in short help (1)")
        self.assertTrue(re.search("Regression test options", outtxt), "Not all option groups included in short help (2)")

    def test_no_args(self):
        """Test using no arguments."""

        fd, logfile = tempfile.mkstemp(suffix='.log', prefix='eb-options-test-')
        os.close(fd)

        try:
            main(args=[], exit_on_error=False, logfile=logfile, keep_logs=True)
        except:
            pass
        outtxt = open(logfile, 'r').read()
        os.remove(logfile)  # clean up log file left behind by main

        error_msg = "Please provide one or multiple easyconfig files,"
        error_msg += " or use software build options to make EasyBuild search for easyconfigs"
        self.assertTrue(re.search(error_msg, outtxt), "Suitable error message when eb is run without arguments")


def suite():
    """ returns all the testcases in this module """
    return TestLoader().loadTestsFromTestCase(CommandLineOptionsTest)

if __name__ == '__main__':
    unittestmain()