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

# Utility rule file for tar_lib.

# Include the progress variables for this target.
include CMakeFiles/tar_lib.dir/progress.make

CMakeFiles/tar_lib:
	/usr/bin/cmake -E tar czf pblib_static.tgz libpblib.a lib/ manual/pblib.pdf LICENSE pbencoder manual/pblib.pdf BasicPBSolver/pbsolver VERSION

tar_lib: CMakeFiles/tar_lib
tar_lib: CMakeFiles/tar_lib.dir/build.make

.PHONY : tar_lib

# Rule to build all files generated by this target.
CMakeFiles/tar_lib.dir/build: tar_lib

.PHONY : CMakeFiles/tar_lib.dir/build

CMakeFiles/tar_lib.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/tar_lib.dir/cmake_clean.cmake
.PHONY : CMakeFiles/tar_lib.dir/clean

CMakeFiles/tar_lib.dir/depend:
	cd /root/1-Dollo-Phylogeny-Solution-Sampler/pblib && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/1-Dollo-Phylogeny-Solution-Sampler/pblib /root/1-Dollo-Phylogeny-Solution-Sampler/pblib /root/1-Dollo-Phylogeny-Solution-Sampler/pblib /root/1-Dollo-Phylogeny-Solution-Sampler/pblib /root/1-Dollo-Phylogeny-Solution-Sampler/pblib/CMakeFiles/tar_lib.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/tar_lib.dir/depend

