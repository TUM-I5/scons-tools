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

def CheckPkgconfig(context, lib, opt):
	"""Run pkg-config and return parsed flags"""

	context.Message('Checking whether pkg-config knows ' + lib + '... ')

	def parse_func(env, cmd):
		return env.ParseFlags(cmd)

	try:
		flags = context.env.ParseConfig([context.env['PKG_CONFIG'], '--silence-errors'] + opt + [lib], parse_func)
	except OSError:
		flags = False

	context.Result(bool(flags))
	return flags


def parse(conf, lib, opt = ['--libs']):
	"""Parses and returns options from pkg-config"""

	if 'PKG_CONFIG' not in conf.env:
		conf.AddTest('CheckProg', utils.checks.CheckProg)
		conf.env['PKG_CONFIG'] = conf.CheckProg('pkg-config')

	if not conf.env['PKG_CONFIG']:
		return None

	conf.AddTest('CheckPkgconfig', CheckPkgconfig)
	return conf.CheckPkgconfig(lib, opt)
