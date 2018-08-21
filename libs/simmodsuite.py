#! /usr/bin/python

## @file
# This file is part of scons-tools.
#
# @author Sebastian Rettenberger <sebastian.rettenberger@tum.de>
#
# @copyright Copyright (c) 2017, Technische Universitaet Muenchen.
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

import utils.checks

def tryLibPath(env, libPath, mpiWrapper, setRpath):
	envTmp = env.Clone()

	conf = envTmp.Configure()
	utils.checks.addDefaultTests(conf)

	envTmp.AppendUnique(LIBPATH=libPath)

	# Add path for parasolid library
	psLibPath = [p for p in map(lambda p: os.path.join(p, 'psKrnl'), libPath) if os.path.exists(p)]
	envTmp.AppendUnique(LIBPATH=psLibPath)
	if setRpath:
		envTmp.AppendUnique(RPATH=psLibPath)

	# TODO check all headers
	# TODO not all libraries may be available/required
	libs = [
		('SimAdvMeshing', 'SimAdvMeshing.h'),
		('SimMeshing', 'MeshSim.h'),
		('SimField', 'SimField.h'),
		('SimDiscrete', 'SimDiscrete.h'),
		('SimMeshTools', 'SimMeshTools.h'),
		(['SimParasolid260', 'SimParasolid270', 'SimParasolid280', 'SimParasolid300'], None),
		('SimPartitionedMesh-mpi', 'SimPartitionedMesh.h'),
		('SimPartitionWrapper-'+mpiWrapper, None),
		('SimModel', 'SimModel.h'),
		('pskernel', None)
	]

	try:
		for l in libs:
			if l[1]:
				if not conf.CheckLibWithHeader(l[0], l[1], 'c++'):
					return False
			else:
				if not conf.CheckLib(l[0]):
					return False
	finally:
		conf.Finish()

	env.Replace(**envTmp.Dictionary())
	return True


def find(env, required=True, mpiLib='mpich2', modifyRpath=True):
	for lib in ['x64_rhel7_gcc48', 'x64_rhel6_gcc44', 'x64_rhel5_gcc41']:
		libPath = [p for p in map(lambda p: os.path.join(p, lib), env['LIBPATH']) if os.path.exists(p)]
		if not libPath:
			# This library directory does not exist -> try next
			continue

		utils.checks.display('checking for simmodeler libraries in %s ...' % lib)
		if tryLibPath(env, libPath, mpiLib, modifyRpath):
			return True

	# Not found
	if required:
		utils.checks.error('Could not find SimModSuite')
		env.Exit(1)

	return False
