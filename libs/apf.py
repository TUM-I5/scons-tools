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

import utils.checks

def find(env, required=True, simmetrix=False, zoltan=False):
	conf = env.Configure()
	utils.checks.addDefaultTests(conf)

	# Libs required to couple SimModSuite (simmetrix)
	simmetrixLibs = [('gmi_sim', 'gmi_sim.h'), ('apf_sim', 'apfSIM.h')]
	# Libs required to couple Zoltan
	zoltanLibs = [('apf_zoltan', 'apfZoltan.h')]
	# Other APF libs
	libs = [('gmi', 'gmi.h'), ('mds', 'apfMDS.h'), ('ma', 'ma.h'),
		('apf', 'apf.h'), ('pcu', 'PCU.h'),
		('lion','lionCompress.h'), ('mth','mth.h')]

	if zoltan:
		libs = zoltanLibs + libs
	if simmetrix:
		libs = simmetrixLibs + libs

	for lib in libs:
		if not conf.CheckLibWithHeader(lib[0], lib[1], 'c++'):
			if required:
				utils.checks.error('Could not find %s' % lib[0])
				env.Exit(1)
			else:
				conf.Finish()
				return False

	conf.Finish()
	return True