#!/usr/bin/env python 

# CMake builder
# Adapted from https://bitbucket.org/scons/scons/wiki/MakeBuilder
#
# Parameters:
#    CMakeProject -- SCons Dir representing the external project. REQUIRED.
#    CMakeBuildDir -- SCons Dir pointing to the working directory used during build.
#    CMakeCmd -- The 'cmake' executable to run.
#                Default: cmake
#    MakeCmd -- The 'make' executable to run.
#               Default: make
#    CMakeOpts -- Options to pass on the CMake command line.
#                 Default: none

import os
import sys
import subprocess

from SCons.Script import *

def parameters(target, source, env):
  """Assemble CMake parameters."""

  if 'CMakeProject' in env.Dictionary().keys():
    cMakeProject = os.path.abspath( env.subst(str(env['CMakeProject'])) )
  else:
    print "CMake builder requires CMakeProject variable"
    Exit(1)

  cMakeCmd = 'cmake'
  if 'CMakeCmd' in env.Dictionary().keys():
    cMakeCmd = env.subst(env['CMakeCmd'])

  cMakeOpts = None
  if 'CMakeOpts' in env.Dictionary().keys():
    cMakeOpts = env.subst(env['CMakeOpts'])

  if 'CMakeBuildDir' in env.Dictionary().keys():
    cMakeBuildDir = os.path.abspath( env.subst(str(env['CMakeBuildDir'])) )
  else:
    cMakeBuildDir = os.path.split(str(target[0]))[0]

  if not os.path.exists(cMakeBuildDir):
    os.makedirs(cMakeBuildDir)

  makeCmd = 'make'
  if 'MakeCmd' in env.Dictionary().keys():
    makeCmd = env.subst(env['MakeCmd'])

  return (cMakeProject, cMakeCmd, cMakeOpts, cMakeBuildDir, makeCmd)

def message(target, source, env):
  """Return a pretty make message"""

  (cMakeProject, cMakeCmd, cMakeOpts, cMakeBuildDir, makeCmd) = parameters(target, source, env)

  return 'cd {} && {} {} {} && {} -j {}'.format(cMakeBuildDir, cMakeCmd, ' '.join(cMakeOpts) if cMakeOpts != None else '', cMakeProject, makeCmd, GetOption('num_jobs'))

def printSubprocess(process):
  while True:
    nextline = process.stdout.readline()
    if nextline == '' and process.poll() is not None:
      break
    sys.stdout.write(nextline)
    sys.stdout.flush()
  output = process.communicate()[0]

def builder(target, source, env):
  """Run cmake and make."""

  (cMakeProject, cMakeCmd, cMakeOpts, cMakeBuildDir, makeCmd) = parameters(target, source, env)

  # Make sure there's a directory to run make in
  if len(cMakeProject) == 0:
    print 'No path specified'
  if not os.path.exists(cMakeProject):
    print 'Path %s not found' % cMakeProject

  # Build up the command and its arguments in a list
  cmakeAssembled = [ cMakeCmd ]

  if cMakeOpts:
    cmakeAssembled.extend(cMakeOpts)

  cmakeAssembled.append(cMakeProject)

  # cmake
  cmake = subprocess.Popen( cmakeAssembled,
                            cwd = cMakeBuildDir,
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE,
                            universal_newlines=True )
  printSubprocess(cmake)

  makeAssembled = [ makeCmd, '-j', str(GetOption('num_jobs'))]

  # make
  make = subprocess.Popen( makeAssembled,
                           cwd = cMakeBuildDir,
                           stdout = subprocess.PIPE,
                           stderr = subprocess.PIPE )
  printSubprocess(make)

  return make.returncode

def generate(env, **kwargs):
  env['BUILDERS']['CMake'] = env.Builder(action = env.Action(builder, message))

def exists(env):
  return True
