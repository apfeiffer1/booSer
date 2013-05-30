#!/usr/bin/env python
# encoding: utf-8
"""
makeSerialAll.py

Mainly based on the example found on:

http://eli.thegreenplace.net/2011/07/03/parsing-c-in-python-with-clang/#id9

Uses the python bindings to libclang to parse the header files and extract the
information about class/struct members. Update the file in-place with the necessary 
member function for an intrusive archival using boost::serialize.

ToDo: - fix handling of classes in namespaces
	  - fix handling of class/struct/enum defined in same line (i.e. the ending '};' is on the same line)
	  - check and update handling of non-trivial issues (abstract base classes, template instantiations)

Created by Andreas Pfeiffer on 2013-05-22.
Copyright (c) 2013 CERN. All rights reserved.
"""

import sys
import os
import re
import glob
import getopt

import clang.cindex
from clang.cindex import CursorKind

from pprint import pprint

help_message = '''
The help message goes here.
'''

baseIncludes = '''
// for the serialization 
#include <boost/serialization/access.hpp> 
#include <boost/serialization/vector.hpp> 
#include <boost/serialization/string.hpp> 
#include <boost/serialization/map.hpp> 
'''
inheritIncludes = '''
#include <boost/serialization/base_object.hpp>
#include <boost/serialization/export.hpp>
'''
serialBase = '''
     // method 1 : invoke base class serialization
     ar & boost::serialization::base_object< %s >(*this);
'''
exportStmt = '''BOOST_CLASS_EXPORT_GUID(%s, "%s");
'''

def get_diag_info(diag):
    return { 'severity' : diag.severity,
             'location' : diag.location,
             'spelling' : diag.spelling,
             'ranges' : diag.ranges,
             'fixits' : diag.fixits }

globalDebug = False
showDetails = -1

itemList = {}

def getAncestors(node):
    if not node: return ''
    parent = node.getCursorSemanticParent()
    if not parent: return ''
    # print "parent is ", parent.displayname, ' type ', parent.kind
    if parent.kind == CursorKind.TRANSLATION_UNIT: return ''
    
    if parent == clang.cindex.Cursor_null():
        return ''
    else:
        return getAncestors(parent)+'::'+parent.displayname

def showAll():
    for k, v in itemList.items():
        print k, v

def writeFile(fileNameIn):
    
    haveSerials = writeSerialFileInvasive(fileNameIn)
    if haveSerials: writeTestFile(fileNameIn)

def writeTestFile(fileNameIn):
    
    filePath     = os.path.dirname(fileNameIn)
    fileBaseName = os.path.basename(fileNameIn)
    fileName, fileExt  = os.path.splitext(fileBaseName)
    
    # if len(itemList.keys()) > 1:
    #    print "WARNING: more than one class found here : ", fileNameIn, itemList.keys()
    testClass = itemList.keys()[0]
    
    content = """

#include <fstream>

#include <boost/archive/tmpdir.hpp>
#include <boost/archive/text_iarchive.hpp>
#include <boost/archive/text_oarchive.hpp>

#include <boost/serialization/base_object.hpp>
#include <boost/serialization/utility.hpp>
#include <boost/serialization/list.hpp>
#include <boost/serialization/assume_abstract.hpp>

#include "CondFormats/Objects/interface/%s.h"

int main() {
    // create and open a character archive for output
    std::string arFileName = "%s.boostArchive";
    std::ofstream ofs(arFileName.c_str());
    
    // create class instance
    %s t1;
    // save data to archive
    {
        boost::archive::text_oarchive oa(ofs);
        // write class instance to archive
        oa << t1;
        // archive and stream closed when destructors are called
    }
    
    // ... some time later restore the class instance to its orginal state
    %s tNew;
    {
        // create and open an archive for input
        std::ifstream ifs(arFileName.c_str());
        boost::archive::text_iarchive ia(ifs);
        // read class state from archive
        ia >> tNew;;
        // archive and stream closed when destructors are called
    }
    return 0;
}

""" % (fileName, fileName, testClass, testClass)
    
    fullFilePath = os.path.join( filePath.replace('interface', 'test'), fileName+'_testSerialize.cpp')
    print "writing test code to ", fullFilePath
    
    outFile = open(fullFilePath, 'w')
    outFile.write(content)
    outFile.close()
    
    #-ap: not any more :
    #-ap # update also the buildfile:
    #-ap outFile = open(os.path.join( filePath.replace('interface', 'test'), 'BuildFile.xml'), 'a')
    #-ap outFile.write('<bin   name="%s_testSerialize" file="%s_testSerialize.cpp"></bin>\n' % (fileName, fileName))
    #-ap outFile.close()
    #-ap: end

def writeSerialFileInvasive(fileNameIn):
    
    filePath     = os.path.dirname(fileNameIn)
    fileBaseName = os.path.basename(fileNameIn)
    fileName, fileExt  = os.path.splitext(fileBaseName)
    
    contentTemplate = """

  // class/struct : %s
  friend class boost::serialization::access;
 private:
   // When the class Archive corresponds to an output archive, the
   // & operator is defined similar to <<.  Likewise, when the class Archive
   // is a type of input archive the & operator is defined similar to >>.
   template<class Archive>
   void serialize(Archive & ar, const unsigned int version) {   //BASESTMT//
%s   }
""" 
    content = {}
    for k, v in itemList.items():
        print '++> handling class/struct ', k, v
        arStatements = ''
        for item in v:
            arStatements += '     ar & '+str(item)+';\n'
        
        content[k.split(':')[-1]] = contentTemplate % (k.split(':')[-1], arStatements)

    print "content has ", len(content.keys()), 'items'
    if globalDebug:
        for k, v in content.items():
            print "\t", k, ' : ', v

    if not itemList:
        print "No members to serialize found in ", fileNameIn
        return False
    
    print "going to call rewrite ... "
    newContent, exports = rewriteContent(fileNameIn, content)
    
    if showDetails > 5: 
        print newContent	
        print exports	
    
    # fullFilePath = os.path.join( filePath, fileName+'_serializeInv.icc')
    # print "writing (invasive) serialize code to ", fullFilePath
    
    fullFilePath = fileNameIn
    print "re-writing with (invasive) serialize code to ", fullFilePath
    
    outFile = open(fullFilePath, 'w')
    outFile.write(newContent)
    outFile.close()
    
    if exports:
    	print "adding exports ", exports
    	# ToDo: add also header file include !!!!
    	expFile = open(os.path.join( filePath, '..', 'src', 'exportStatements.cc'), 'a')
    	expFile.write('#include "'+fileName+'"\n')
    	expFile.write(exports+'\n')
    	expFile.close()
		
    return True

def rewriteContent(fileNameIn, content):

	inFile = open(fileNameIn, 'r')
	inLines = inFile.readlines()
	inFile.close()

	print ":::::> preparing to rewrite ", fileNameIn, len(inLines)
	
	includeRe = re.compile('^\s*#include\s*.*$')
	classStartRe = re.compile('^\s*(class|struct|enum|union)\s*([a-zA-Z].*?)\s\s*(:\s*(public|private|protected)\s*[A-Za-z0-9_<>:]*)?\s*\{?\s*$')
	classEndRe   = re.compile('^\s*\};\s*.*$')
	
	lastInclude = 0
	classEnds   = {}
	actClasses  = []
	derived     = {}
	lastClassEnd = 0
	for index in range(len(inLines)):
		line = inLines[index]
		if includeRe.match(line): lastInclude = index
		classStart = classStartRe.match(line)
		if classStart:
			# print "found new construct: "
			if classStart.group(1).strip() == 'enum': continue
			actClass = classStart.group(2).replace('{', '')
			# print "groups found: ", classStart.groups()
			actClasses.append(actClass)
			if classStart.group(3): # it's a derived class, memorize base class name
				derivedClass = classStart.group(3).split()[-1].replace('{', '')
				derived[actClass] = derivedClass
		if classEndRe.match(line) : 
			classEnds[actClasses.pop()] = index
			if index > lastClassEnd: lastClassEnd = index
		if showDetails > 1:
			print '\n-->', index, line[:-1]
			print '   ', lastInclude, actClasses, classEnds, derived, lastClassEnd

	if globalDebug:
		print '   ', lastInclude, actClasses, classEnds, derived

	outLines = inLines
	outLines[lastInclude] += baseIncludes
	if derived:
		outLines[lastInclude] += inheritIncludes
	for className, index in classEnds.items():
		try:
			serContent = content[className]
			if className in derived.keys():
				baseStmt = serialBase % (derived[className],)
				serContent = serContent.replace('//BASESTMT//', baseStmt )
			else:
				serContent = serContent.replace('BASESTMT', '')
			outLines[index] = serContent + inLines[index] # add back the closing brace plus any comment it may have
			lastClassEnd = index
		except KeyError:  # may have found an enum or the like 
			pass
	
	exports = ''
	if derived:
		for className, index in derived.items():
			exports += exportStmt % (className, className)

	return ''.join(outLines), exports
	
def showNodeInfo(node, parent, userdata, ancestor):
    
    fileName = os.path.basename(node.location.file.name)
    print '> %s [l=%4s, c=%3s] : %25s "%30s" parent: ""%30s""' % (
            fileName,
            node.location.line,
            node.location.column,
            node.kind.name.replace("CursorKind.",''),
            node.displayname,
            parent.displayname,
            ),
    if ancestor:
        print ' semantic parent: ""%s""' % (ancestor,)
    else:
        print ''

def findMembers(node, parent, userdata):
    if node.location.file == None or node.location.file.name.startswith('/usr/') : return 2
    
    if node.location.file.name != userdata['fileName'] : return 2
    
    if showDetails > 5:
        ancestor = getAncestors(node)
        showNodeInfo(node, parent, userdata, ancestor)

    if node.kind == clang.cindex.CursorKind.FIELD_DECL:
        ancestor = getAncestors(node)
        try:
            if ancestor.rindex(':') > ancestor.index('<') :
            	print "WARNING: found template class with embedded members/structs: ", ancestor
            ancestor = ancestor[:ancestor.find('<')]
        except ValueError:
           pass
           
        if ancestor not in itemList.keys():
            itemList[ancestor] = []
        itemList[ancestor].append( node.displayname )  # add member to class
        
        if globalDebug:
            showNodeInfo(node, parent, userdata, ancestor)
    
    return 2 # means continue visiting recursively

def ignoreFile(fileNameIn):

    filePath     = os.path.dirname(fileNameIn)
    fileBaseName = os.path.basename(fileNameIn)

    if fileBaseName[0] in 'ABCDEFGHIJKL': return True

    ignoreList = ['HcalCalibration', 'HcalChannel']
    print 'checking ', fileBaseName, ignoreList
    for item in ignoreList:
    	if item in fileBaseName: return True
    
    return False

def processAll():
    fileList = glob.glob('interface/*.h')
    print 'going to process ', len(fileList), 'files ...'

    for fileName in fileList:
		try:
			process(fileName)
		except Exception, e:
			print "ERROR processing ", fileName
			print "      got: ", str(e)
			print '+'*80

def process(fileName):
    
    # if ignoreFile(fileName): 
    # 	print "already done ... skipping ", fileName
    # 	return

    itemList.clear()
    
    print "\ngoing to process ", fileName
    index = clang.cindex.Index.create()
    tu = index.parse(fileName, args=['-xc++','-I.'])
    
    if tu == None:
        print "ERROR parsing ... ", fileName
        return
    
    diags = map(get_diag_info, tu.diagnostics)
    ignoreDiags = False
    if diags:
        ignoreDiags = ("boost/" in diags[0]['spelling'])
    if diags and not ignoreDiags:
        pprint(('diags', diags))
    
    userData = {'fileName':fileName}
    clang.cindex.Cursor_visit(
            tu.cursor,
            clang.cindex.Cursor_visit_callback(findMembers),
            userData)
    
    if globalDebug: showAll()
    
    writeFile( fileName )

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "havds:", ["help", "all", 'verbose', 'debug', 'showDetails='])
		except getopt.error, msg:
			raise Usage(msg)
		
		# option processing
		global globalDebug
		global showDetails
		doAll = False
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option in ("-h", "--help"):
				raise Usage(help_message)
			if option in ('d', '--debug'):
				globalDebug = True
			if option in ("-s", "--showDetails"):
				showDetails = int(value)
			if option in ("-a", "--all"):
				doAll = True
        
		if doAll:
		    processAll()
		else:
		    process(args[0])
	
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2


if __name__ == "__main__":
    sys.exit(main())
