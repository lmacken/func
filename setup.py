#!/usr/bin/python

from distutils.core import setup
#from setuptools import setup,find_packages

NAME = "func"
VERSION = open("version", "r+").read().split()[0]
SHORT_DESC = "%s remote configuration and management api" % NAME
LONG_DESC = """
A small pluggable xml-rpc daemon used by %s to implement various web services hooks
""" % NAME


if __name__ == "__main__":
 
        manpath    = "share/man/man1/"
        etcpath    = "/etc/%s" % NAME
        etcmodpath = "/etc/%s/modules" % NAME
        initpath   = "/etc/init.d/"
        logpath    = "/var/log/%s/" % NAME
	varpath    = "/var/lib/%s/" % NAME
        rotpath    = "/etc/logrotate.d"
        aclpath    = "%s/minion-acl.d" % etcpath
        setup(
                name="%s" % NAME,
                version = VERSION,
                author = "Lots",
                author_email = "func-list@redhat.com",
                url = "https://hosted.fedoraproject.org/projects/func/",
                license = "GPL",
		scripts = [
                     "scripts/funcd",
		     "scripts/func", 
                     "scripts/func-inventory",
                     "scripts/func-create-module",
		     # "scripts/update-func",
                ],
		# package_data = { '' : ['*.*'] },
                package_dir = {"%s" % NAME: "%s" % NAME
                },
		packages = ["%s" % NAME,
	        	    "%s/minion" % NAME,
			    "%s/overlord" % NAME,
			    "%s/overlord/cmd_modules" % NAME,
                            "%s/overlord/modules" % NAME,
                            "%s/minion/modules" % NAME,
                            # FIXME if there's a clean/easy way to recursively
                            # find modules then by all means do it, for now
                            # this will work.
                            "%s/minion/modules.netapp" % NAME,
                            "%s/minion/modules.netapp.vol" % NAME,
			    "%s/minion/modules.iptables" % NAME
                ],
                data_files = [(initpath, ["init-scripts/funcd"]),
                              (etcpath,  ["etc/minion.conf"]),
                              (manpath,  ["docs/func.1.gz"]),
                              (manpath,  ["docs/func-inventory.1.gz"]),
                              (manpath,  ["docs/funcd.1.gz"]),
			      (rotpath,  ['etc/func_rotate']),
                              (logpath,  []),
			      (etcmodpath,  []),
			      (varpath,  []),
			      (aclpath,  [])
                ],
                description = SHORT_DESC,
                long_description = LONG_DESC
        )

