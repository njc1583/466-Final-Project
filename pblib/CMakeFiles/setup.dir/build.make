# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /root/1-Dollo-Phylogeny-Solution-Sampler/pblib

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /root/1-Dollo-Phylogeny-Solution-Sampler/pblib

# Utility rule file for setup.

# Include the progress variables for this target.
include CMakeFiles/setup.dir/progress.make

CMakeFiles/setup:
	cd BasicPBSolver/ && tar xzf minisat.tgz && cd minisat && cmake . && make -j3 && cd ../.. && cmake . && make -j3 && make fuzzer && make pbo2maxsat && make pbencoder && cd BasicPBSolver/ && cmake . && make -j3

setup: CMakeFiles/setup
setup: CMakeFiles/setup.dir/build.make

.PHONY : setup

# Rule to build all files generated by this target.
CMakeFiles/setup.dir/build: setup

.PHONY : CMakeFiles/setup.dir/build

CMakeFiles/setup.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/setup.dir/cmake_clean.cmake
.PHONY : CMakeFiles/setup.dir/clean

CMakeFiles/setup.dir/depend:
	cd /root/1-Dollo-Phylogeny-Solution-Sampler/pblib && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/1-Dollo-Phylogeny-Solution-Sampler/pblib /root/1-Dollo-Phylogeny-Solution-Sampler/pblib /root/1-Dollo-Phylogeny-Solution-Sampler/pblib /root/1-Dollo-Phylogeny-Solution-Sampler/pblib /root/1-Dollo-Phylogeny-Solution-Sampler/pblib/CMakeFiles/setup.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/setup.dir/depend

