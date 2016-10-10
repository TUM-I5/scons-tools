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

def removeUnknownOptions(args):
	"""Removes compiler options unknown to SCons from the list of arguments"""

	if not SCons.Util.is_List(args):
		args = args.split()

	# TODO extend these if neseccary
	prefixOptions = ['-I', '-D', '-L', '-l']
	def isPrefixOption(arg):
		for o in prefixOptions:
			if arg.startswith(o):
				return True

		return False


	cleaned_args = list(args) # copy all
	for i in xrange(len(args) - 1, -1, -1): # iterate backwards
		if isPrefixOption(args[i]):
			continue

		# Run other tests here

		del cleaned_args[i]

	return ' '.join(cleaned_args)
