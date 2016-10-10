#! /usr/bin/python

## @file
# This file is part of scons-tools.
#
# @author Sebastian Rettenberger <sebastian.rettenberger@tum.de>
#
# @copyright Copyright (c) 2016, Technische Universitaet Muenchen.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import SCons

def _lang2name(lang):
	"""Unify language name"""
	if not lang or lang in ["C", "c"]:
		return "C"
	if lang in ["c++", "C++", "cpp", "CXX", "cxx"]:
		return "C++"

	return None


def _libInEnv(libs, env):
	"""Checks if a libraries is defined in the current environment"""
	try:
		for l in libs:
			if l in env['LIBS']:
				return l
	except KeyError:
		pass

	return False

def display(msg):
	SCons.Util.DisplayEngine()('scons: '+msg)

def error(msg):
	display('error: '+msg)

def CheckProg(context, prog_name):
	"""
	This function is from the latest version of SCons to support
	older SCons version.
	Configure check for a specific program.
	Check whether program prog_name exists in path.  If it is found,
	returns the path for it, otherwise returns None.
	"""

	context.Message("Checking whether %s program exists..." % prog_name)
	path = context.env.WhereIs(prog_name)
	context.Result(bool(path))

	return path

def CheckLib(context, library = None, symbol = "main",
		header = None, language = None, extra_libs = None,
		autoadd = 1):
	"""
	This function is from SCons but extended with additional flags, e.g.
	the extra_libs and avoids duplicate loading of libraries.
	A test for a library. See also CheckLibWithHeader.
	Note that library may also be None to test whether the given symbol
	compiles without flags.
	"""

	if library == []:
		library = [None]

	if not SCons.Util.is_List(library):
		library = [library]

	if symbol == 'main':
		found = _libInEnv(library, context.env)
		if found:
			context.Message("Checking for %s library %s... " % (_lang2name(language), found))
			context.Result(True)
			return True

	# ToDo: accept path for the library
	res = SCons.Conftest.CheckLib(context, library, symbol, header = header,
		language = language, extra_libs = extra_libs, autoadd = autoadd)
	context.did_show_result = 1
	return not res



def CheckLibWithHeader(context, libs, header, language,
		call = None, extra_libs = None, autoadd = 1):
	"""
	This function is from SCons but extended with additional flags, e.g.
	the extra_libs and avoids duplicate loading of libraries.
	Another (more sophisticated) test for a library.
	Checks, if library and header is available for language (may be 'C'
	or 'CXX'). Call maybe be a valid expression _with_ a trailing ';'.
	As in CheckLib, we support library=None, to test if the call compiles
	without extra link flags.
	"""
	prog_prefix, dummy = \
		SCons.SConf.createIncludesFromHeaders(header, 0)

	if libs == []:
		libs = [None]

	if not SCons.Util.is_List(libs):
		libs = [libs]

	found = _libInEnv(libs, context.env)
	if found:
		context.Message("Checking for %s library %s... " % (_lang2name(language), found))
		context.Result(True)
		return True

	res = SCons.Conftest.CheckLib(context, libs, None, prog_prefix,
		call = call, language = language, extra_libs = extra_libs,
		autoadd = autoadd)
	context.did_show_result = 1
	return not res


def addDefaultTests(conf):
	conf.AddTests({
		'CheckProg': CheckProg,
		'CheckLib': CheckLib,
		'CheckLibWithHeader': CheckLibWithHeader
		})