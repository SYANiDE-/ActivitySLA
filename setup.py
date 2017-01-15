from distutils.core import setup
import py2exe, sys, os, argparse

excludeS=['.idea','setup.py','test.py','build.bat','locales']
includeS=['argparse', 'operator']

setup(
    console=['ActivitySLA.py'],
    options={
        "py2exe":{
            "optimize": 2,
            "compressed": True,
            "xref": False,
            "bundle_files": 1,
            "skip_archive": False,
            "ascii": False,
            "excludes": excludeS,
            "includes": includeS
        }
    },
    zipfile = None
)

"""
bundle_files:  (making a *mostly* self-contained executable REQUIRES the following edit):


Thanks to this link (http://sourceforge.net/p/py2exe/bugs/108/), you have to edit site-packages/py2exe/build_exe.py and
add "tcl85.dll" and "tk85.dll" to the dlls_in_exedir list. This will get it to run, although you'll still have the
tcl folders, and those two dlls will be there along-side the exe. But it's way better than bundle_files=3.


Make edit IN:  Python27\Lib\site-packages\py2exe\ build_exe.py


Find and edit the structure to look like this:

self.dlls_in_exedir = [python_dll,
                               "w9xpopen%s.exe" % (is_debug_build and "_d" or ""),
                               "msvcr71%s.dll" % (is_debug_build and "d" or ""),
                               "tcl85.dll",
                               "tk85.dll"]

Confirmed working!
"""