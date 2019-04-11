#! /usr/bin/python

## @file
# This file is part of scons-tools.
#
# @author Carsten Uphoff <uphoff@in.tum.de>
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

def find(env, required=True, parallel=False):
  conf = env.Configure()
  utils.checks.addDefaultTests(conf)

  opt = ['--libs', '--static', '--cflags']
  if parallel:
    flags = utils.pkgconfig.parse(conf, 'asagi', opt)
  else:
    flags = utils.pkgconfig.parse(conf, 'asagi_nompi', opt)
    env.Append(CPPDEFINES=['ASAGI_NOMPI'])

  if not flags:
    if required:
      utils.checks.error('Could not find ASAGI with pkg-config: Make sure pkg-config is installed and PKG_CONFIG_PATH contains asagi.pc')
      env.Exit(1)
    else:
      conf.Finish()
      return False
    
  utils.pkgconfig.appendPathes(env, flags)
  
  if not conf.CheckLibWithHeader(flags['LIBS'][0], 'asagi.h', 'c++', extra_libs=flags['LIBS'][1:]):
		if required:
			utils.checks.error('Could not find ASAGI')
			env.Exit(1)
		else:
			conf.Finish()
			return False

  conf.Finish()
  return True
