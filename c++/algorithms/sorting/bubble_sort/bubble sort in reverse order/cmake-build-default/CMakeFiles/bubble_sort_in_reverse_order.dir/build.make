# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.20

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /Applications/CLion.app/Contents/bin/cmake/mac/bin/cmake

# The command to remove a file.
RM = /Applications/CLion.app/Contents/bin/cmake/mac/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = "/Users/shrekulka/Desktop/C++/algorithms/sorting/bubble_sort/bubble sort in reverse order"

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = "/Users/shrekulka/Desktop/C++/algorithms/sorting/bubble_sort/bubble sort in reverse order/cmake-build-default"

# Include any dependencies generated for this target.
include CMakeFiles/bubble_sort_in_reverse_order.dir/depend.make
# Include the progress variables for this target.
include CMakeFiles/bubble_sort_in_reverse_order.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/bubble_sort_in_reverse_order.dir/flags.make

CMakeFiles/bubble_sort_in_reverse_order.dir/main.cpp.o: CMakeFiles/bubble_sort_in_reverse_order.dir/flags.make
CMakeFiles/bubble_sort_in_reverse_order.dir/main.cpp.o: ../main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="/Users/shrekulka/Desktop/C++/algorithms/sorting/bubble_sort/bubble sort in reverse order/cmake-build-default/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/bubble_sort_in_reverse_order.dir/main.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/bubble_sort_in_reverse_order.dir/main.cpp.o -c "/Users/shrekulka/Desktop/C++/algorithms/sorting/bubble_sort/bubble sort in reverse order/main.cpp"

CMakeFiles/bubble_sort_in_reverse_order.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/bubble_sort_in_reverse_order.dir/main.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "/Users/shrekulka/Desktop/C++/algorithms/sorting/bubble_sort/bubble sort in reverse order/main.cpp" > CMakeFiles/bubble_sort_in_reverse_order.dir/main.cpp.i

CMakeFiles/bubble_sort_in_reverse_order.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/bubble_sort_in_reverse_order.dir/main.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "/Users/shrekulka/Desktop/C++/algorithms/sorting/bubble_sort/bubble sort in reverse order/main.cpp" -o CMakeFiles/bubble_sort_in_reverse_order.dir/main.cpp.s

# Object files for target bubble_sort_in_reverse_order
bubble_sort_in_reverse_order_OBJECTS = \
"CMakeFiles/bubble_sort_in_reverse_order.dir/main.cpp.o"

# External object files for target bubble_sort_in_reverse_order
bubble_sort_in_reverse_order_EXTERNAL_OBJECTS =

bubble_sort_in_reverse_order: CMakeFiles/bubble_sort_in_reverse_order.dir/main.cpp.o
bubble_sort_in_reverse_order: CMakeFiles/bubble_sort_in_reverse_order.dir/build.make
bubble_sort_in_reverse_order: CMakeFiles/bubble_sort_in_reverse_order.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir="/Users/shrekulka/Desktop/C++/algorithms/sorting/bubble_sort/bubble sort in reverse order/cmake-build-default/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable bubble_sort_in_reverse_order"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/bubble_sort_in_reverse_order.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/bubble_sort_in_reverse_order.dir/build: bubble_sort_in_reverse_order
.PHONY : CMakeFiles/bubble_sort_in_reverse_order.dir/build

CMakeFiles/bubble_sort_in_reverse_order.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/bubble_sort_in_reverse_order.dir/cmake_clean.cmake
.PHONY : CMakeFiles/bubble_sort_in_reverse_order.dir/clean

CMakeFiles/bubble_sort_in_reverse_order.dir/depend:
	cd "/Users/shrekulka/Desktop/C++/algorithms/sorting/bubble_sort/bubble sort in reverse order/cmake-build-default" && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" "/Users/shrekulka/Desktop/C++/algorithms/sorting/bubble_sort/bubble sort in reverse order" "/Users/shrekulka/Desktop/C++/algorithms/sorting/bubble_sort/bubble sort in reverse order" "/Users/shrekulka/Desktop/C++/algorithms/sorting/bubble_sort/bubble sort in reverse order/cmake-build-default" "/Users/shrekulka/Desktop/C++/algorithms/sorting/bubble_sort/bubble sort in reverse order/cmake-build-default" "/Users/shrekulka/Desktop/C++/algorithms/sorting/bubble_sort/bubble sort in reverse order/cmake-build-default/CMakeFiles/bubble_sort_in_reverse_order.dir/DependInfo.cmake" --color=$(COLOR)
.PHONY : CMakeFiles/bubble_sort_in_reverse_order.dir/depend

