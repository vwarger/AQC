#!/bin/env python

from sys import argv
from os import walk, path
from re import compile, M, I
from warnings import warn

pathre = compile("^(\s*[A-Za-z_]+(?:\(\d+\))?\s*=\s*')([^']+)('.*)", M + I)
def find(name, rpath):
    """
    Given a file name, find its basename in rpath
    or a subdirectory of rpath and return the
    path
    """
    bname = path.basename(name)
    for root, dirs, files in walk(rpath, followlinks = True):
        if bname in files:
            return path.join(root, bname)
    else:
	return name

def replacep(matchobj):
    """
    Given a match object that represents a key,
    path value, and trailing characters from a namelist
    line, replacep will replace the path value with
    a local path value if the file can be found.
    
    Namelist line: "A = '/path/B' # B is the value of a;"
    matchobj.groups(): ["A = '", "/path/B", "' # B is the value of a;"]

    """
    global root
    # Get a list of key, path, and traling characters
    keypath = list(matchobj.groups())
    # Make a copy
    oldkeypath = [i_ for i_ in keypath]
    
    # if '/' is in the path value, then it is a path
    if '/' in keypath[1]:
        keypath[1] = find(keypath[1], root)
    
    # Check if the new keypath has been updated
    # and report to the user
    if oldkeypath != keypath:
        print 'Updated: %s from %s to %s' % (keypath[0], oldkeypath[1], keypath[1])
    # Return a new string that may be the same as the old string
    return ''.join(keypath)

if __name__ == '__main__':
    args = [i_ for i_ in argv]
    rootopt = [ia for ia, arg in enumerate(args) if '--root' in arg]
    root = '..'
    if len(rootopt) > 0:
        if len(rootopt) > 1:
            warn('Only one --root is allowed; the last overwrites all')
        for rooti in rootopt:
            root = args[rooti].split('=')[-1]
        for rooti in rootopt[::-1]:
            args.pop(rooti)
        print 'New root is:', root

    if len(args) == 1 or '-h' in args or '--help' in args:
	print 'Usage: %s [--root=..] namelistpath...\n\n\tnamelistpath is the path to a namelist\n\t\twith paths that should be updated\n\n\t--root=newpath sets the root folder for\n\t\tupdating paths to \n\t\tnewpath; newpath is .. by default.' % args[0]
        exit()
    
    # For each argument passed to the script,
    # update paths based on locally available paths
    for arg in args[1:]:
        print 'Replacing old paths with local paths for:', arg
        oldtext = file(arg, 'r').read()
        newtext = pathre.sub(replacep, oldtext)
        if oldtext != newtext:
            file(arg, 'w').write(newtext)
        else:
            warn('No replacements made')
    
