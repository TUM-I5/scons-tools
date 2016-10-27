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

# The preprocessor macro is defined as the date of the release
# see here for release dates: http://openmp.org/wp/openmp-specifications/
__openmp_version2date = {
	'1.0': 199810,
	'2.0': 200211,
	'2.5': 200505,
	'3.0': 200803,
	'3.1': 201107,
	'4.0': 201307,
	'4.5': 201511}

# This will only compile if OpenMP version is large enough
__openmp_prog_src = """
#if _OPENMP >= %s
int main(int argc, char** argv) {
#endif
	return 0;
}
"""

def __CheckOmpVersion(context, version):
	context.Message("Checking for OpenMP v%s... " % (version,))
	try:
		omp_date = __openmp_version2date[version]
	except KeyError:
		utils.checks.error('Unknown OpenMP version %s' % (version,))
		context.env.Exit(1)

	ret = context.TryCompile(__openmp_prog_src % (omp_date,), '.c')
	context.Result(ret)

	return ret

def find(env, required=True, version='1.0', **kw):
	"""version: minimal required OpenMP version"""

	if env.GetOption('help') or env.GetOption('clean'):
		return

	# Work on a copy of env
	env = env.Clone()

	conf = env.Configure()
	conf.AddTests({'CheckOmpVersion': __CheckOmpVersion})

	env.Append(CFLAGS=['-fopenmp'])
	if not conf.CheckOmpVersion(version):
		if required:
			utils.checks.error('OpenMP version %s not supported' % (version,))
			env.Exit(1)
		else:
			conf.Finish()
			return False

	conf.Finish()
	return True

