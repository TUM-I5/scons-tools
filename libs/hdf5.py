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

import utils.checks
import utils.compiler
import utils.pkgconfig

__hdf5_api_check = """
#include <hdf5.h>

#ifdef H5_USE_%s_API
int main(int argc, char* argv) {
#endif
	return 0;
}
"""

def CheckAPIVersion(context, api):
	context.Message('Checking for HDF5 v%s API... ' % (api,))
	ret = context.TryCompile(__hdf5_api_check % (api,), '.c')
	context.Result(ret)

	return ret

def find(env, required=True, parallel=False, hl=True, api=18):
	conf = env.Configure()
	utils.checks.addDefaultTests(conf)
	conf.AddTests({'CheckAPIVersion': CheckAPIVersion})

	# Find h5cc or h5pcc
	h5ccs = ['h5cc', 'h5pcc']
	if parallel:
		# Change order if parallel program is requested
		h5ccs[0], h5ccs[1] = h5ccs[1], h5ccs[0]

	for h5cc in h5ccs:
		h5cc = conf.CheckProg(h5cc)
		if h5cc:
			break

	if h5cc:
		# Parse the output from the h5cc compiler wrapper
		def parse_func(env, cmd):
			# remove the compiler
			cmd = cmd.partition(' ')[2]
			# remove unknown arguments
			cmd = utils.compiler.removeUnknownOptions(cmd)
			return env.ParseFlags(cmd)
		flags = env.ParseConfig([h5cc, '-show', '-shlib'], parse_func)
	else:
		# Try pkg-config
		hdf5s = ['hdf5_hl', 'hdf5_hl_parallel']
		if parallel:
			hdf5s[0], hdf5s[1] = hdf5s[1], hdf5s[0]
		for hdf5 in hdf5s:
			flags = utils.pkgconfig.parse(conf, hdf5)
			if flags:
				break

		if not flags:
			if required:
				print 'Could not find h5cc or h5pcc. Make sure the path to the HDF5 library is correct!'
				env.Exit(1)
			else:
				conf.Finish()
				return False

	utils.pkgconfig.appendPathes(env, flags)

	if not conf.CheckLibWithHeader(flags['LIBS'][0], 'hdf5.h', 'c', extra_libs=flags['LIBS'][1:]):
		if required:
			utils.checks.error('Could not find the HDF5 library')
			env.Exit(1)
		else:
			conf.Finish()
			return False

	if api:
		ret = conf.CheckAPIVersion(16)
		if api == 18 and ret:
			# Redefine all macros
			conf.env.Append(CPPDEFINES=['H5Dcreate_vers=2',
				'H5Dopen_vers=2',
				'H5Gcreate_vers=2',
				'H5Gopen_vers=2',
				'H5Acreate_vers=2',
				'H5Eget_auto_vers=2',
				'H5Eset_auto_vers=2'])
			# TODO add more
		elif api == 16 and not ret:
			# Force 16 API
			conf.env.Append(CPPDEFINES=['H5_USE_16_API'])

	conf.Finish()
	return True