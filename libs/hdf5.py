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

import utils.checks
import utils.compiler
import utils.pkgconfig

def find(env, required=True, parallel=False, hl=True, **kw):
	if env.GetOption('help') or env.GetOption('clean'):
		return

	conf = env.Configure()
	utils.checks.addDefaultTests(conf)

	# Find h5cc or h5pcc
	h5ccs = ['h5cc', 'h5pcc']
	if parallel:
		# Change order if parallel program is requested
		h5ccs[0], h5ccs[1] = h5ccs[1], h5ccs[0]

	for h5cc in h5ccs:
		h5cc = conf.CheckProg(h5cc)
		if h5cc:
			break

	if not h5cc:
		if required:
			utils.checks.error('Cannot find h5cc or h5pcc: Make sure the path to the HDF5 library is correct')
			env.Exit(1)
		else:
			conf.Finish()
			return False


	# Parse the output from the h5cc compiler wrapper
	def parse_func(env, cmd):
		# remove the compiler
		cmd = cmd.partition(' ')[2]
		# remove unknown arguments
		cmd = utils.compiler.removeUnknownOptions(cmd)
		return env.ParseFlags(cmd)
	flags = env.ParseConfig([h5cc, '-show', '-shlib'], parse_func)

	utils.pkgconfig.appendPathes(env, flags)

	if not conf.CheckLibWithHeader(flags['LIBS'][0], 'hdf5.h', 'c', extra_libs=flags['LIBS'][1:]):
		if required:
			utils.checks.error('Could not find the HDF5 library')
			env.Exit(1)
		else:
			conf.Finish()
			return False

	conf.Finish()
	return True