#! /usr/bin/python

## @file
# This file is part of scons-tools.
#
# @author Sebastian Rettenberger <sebastian.rettenberger@tum.de>
#
# @copyright Copyright (c) 2016-2017, Technische Universitaet Muenchen.
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

import os
import SCons

import checks

# Helper function for the prefix path variable
def _pathListExists(key, value, env):
    for path in env[key]:
        SCons.Script.PathVariable.PathExists(key, path, env)

# Helper function for the prefix path variable
def _pathToList(value):
    if not value or value == 'none':
        return []

    return value.split(os.path.pathsep)

class Variables(SCons.Variables.Variables):
	"""Extends the SCons.Variables.Variables with additional functions"""

	def __init__(self):
		SCons.Variables.Variables.__init__(self, args=SCons.Script.ARGUMENTS)

	def ParseVariableFile(self, varname='config', description='location of the python file, which contains the build variables'):
		"""Load values from an external python file specified in varname"""
		self.AddVariables(SCons.Script.PathVariable(varname, description, None, SCons.Script.PathVariable.PathIsFile))

		env = SCons.Script.Environment(variables=self)
		if varname in env:
			self.files.append(env[varname])

	def AddBuildType(self):
		self.AddVariables(SCons.Script.EnumVariable('buildType', 'build type of the compilation', 'release',
			allowed_values=('debug', 'relWithDebInfo', 'release')))

	def AddPrefixPathVariable(self):
		self.AddVariables(('prefixPath',
			'Used when searching for include files, binaries or libraries ( /prefix/path1'+os.path.pathsep+'/prefix/path2 )',
			None,
			_pathListExists,
			_pathToList))

	def AddCompilerVariable(self, ccHint='C compiler', cxxHint='C++ compiler'):
		"""Add option to set compiler executables"""
		self.AddVariables(SCons.Script.PathVariable('cc', ccHint, None, SCons.Script.PathVariable.PathAccept),
			SCons.Script.PathVariable('cxx', cxxHint, None, SCons.Script.PathVariable.PathAccept))

	def SetPrefixPathes(self, env, binpath=False, rpath=True, pkgconfigpath=True):
		"""Configures lib path, include path, bin path, rpath, pkgconfig path from the variable 'prefixPath'"""
		if not 'prefixPath' in env:
			return

		# Append include/lib and add them to the list if they exist
		incPathes = [p for p in map(lambda p: os.path.join(p, 'include'), env['prefixPath']) if os.path.exists(p)]
		libPathes = [p for p in map(lambda p: os.path.join(p, 'lib'), env['prefixPath']) if os.path.exists(p)]

		env.AppendUnique(CPPPATH=incPathes)
		env.AppendUnique(LIBPATH=libPathes)
		if binpath:
			binPathes = [p for p in map(lambda p: os.path.join(p, 'bin'), env['prefixPath']) if os.path.exists(p)]
			env.PrependENVPath('PATH', binPathes)
		if rpath:
			env.AppendUnique(RPATH=libPathes)
		if pkgconfigpath:
			pkgPathes = [p for p in map(lambda p: os.path.join(p, 'lib', 'pkgconfig'), env['prefixPath']) \
					if os.path.exists(p)] + \
				[p for p in map(lambda p: os.path.join(p, 'share', 'pkgconfig'), env['prefixPath']) \
					if os.path.exists(p)]

			env.PrependENVPath('PKG_CONFIG_PATH', pkgPathes)

	def SetCompiler(self, env):
		if 'cc' in env:
			env['CC'] = env['cc']
		if 'cxx' in env:
			env['CXX'] = env['cxx']

	def SetHelpText(self, env):
		SCons.Script.Help(self.GenerateHelpText(env))

	def CheckUnknownVariables(self, env, errorMsg='The following build variables are unknown: %s', exitCode=1):
		unknownVariables = self.UnknownVariables()

		# exit in the case of unknown variables
		if unknownVariables:
			checks.error(errorMsg % ', '.join(unknownVariables.keys()))
			if not SCons.Script.GetOption('help'):
				# Exist only if we are not printing the help message
				env.Exit(exitCode)



