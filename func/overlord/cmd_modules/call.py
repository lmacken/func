"""
call func method invoker

Copyright 2007, Red Hat, Inc
see AUTHORS

This software may be freely redistributed under the terms of the GNU
general public license.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""


import optparse
import pprint
import xmlrpclib

from func.overlord import client
from func.overlord import base_command

DEFAULT_FORKS = 1

class Call(base_command.BaseCommand):
    name = "call"
    usage = "call module method name arg1 arg2..."
    def addOptions(self):
        self.parser.add_option("-v", "--verbose", dest="verbose",
                               action="store_true")
        self.parser.add_option("-x", "--xmlrpc", dest="xmlrpc",
                               help="output return data in XMLRPC format",
                               action="store_true")
        self.parser.add_option("", "--raw", dest="rawprint",
                               help="output return data using Python print",
                               action="store_true")
        self.parser.add_option("-j", "--json", dest="json",
                               help="output return data using JSON",
                               action="store_true")
        self.parser.add_option("-p", "--pickle", dest="pickle",
                               help="output return data in python pickle format",
                               action="store_true")
        self.parser.add_option("-f", "--forks", dest="forks",
                               help="how many parallel processes?  (default 1)",
                               default=DEFAULT_FORKS)

    def handleOptions(self, options):
        self.options = options
        self.verbose = options.verbose

        # I'm not really a fan of the "module methodname" approach
        # but we'll keep it for now -akl

    def parse(self, argv):
        self.argv = argv

        return base_command.BaseCommand.parse(self, argv)
        

    def format_return(self, data):
        """
        The call module supports multiple output return types, the default is pprint.
        """
        
        if self.options.xmlrpc:
            return xmlrpclib.dumps((data,""))

        if self.options.json:
            try:
                import simplejson
                return simplejson.dumps(data)
            except ImportError:
                print "WARNING: json support not found, install python-simplejson"
                return data

        if self.options.rawprint:
            return data

        if self.options.pickle:
            import pickle
            return pickle.dumps(data)

        return  pprint.pformat(data)

    def do(self, args):

        # I'm not really a fan of the "module methodname" approach
        # but we'll keep it for now -akl

        # I kind of feel like we shouldn't be parsing args here, but I'm
        # not sure what the write place is -al;
        self.module           = args[0]
        if len(args) > 1:
            self.method       = args[1]
        else:
            self.method       = None
        if len(args) > 2:
            self.method_args  = args[2:]
        else:
            self.method_args  = []

        # this could get weird, sub sub classes might be calling this
        # this with multiple.parentCommand.parentCommands...
        # maybe command.py needs a way to set attrs on subCommands?
        # or some sort of shared datastruct?
        #        self.getOverlord()


        self.interactive = False
        
        self.server_spec = self.parentCommand.server_spec
        self.getOverlord()
        

        results = self.overlord_obj.run(self.module, self.method, self.method_args)

        # TO DO: add multiplexer support
        # probably as a higher level module.

        # dump the return code stuff atm till we figure out the right place for it
        foo =  self.format_return(results)
        print foo

        # nothing really makes use of this atm -akl
        return foo
