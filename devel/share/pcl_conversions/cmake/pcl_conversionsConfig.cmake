# generated from catkin/cmake/template/pkgConfig.cmake.in

# append elements to a list and remove existing duplicates from the list
# copied from catkin/cmake/list_append_deduplicate.cmake to keep pkgConfig
# self contained
macro(_list_append_deduplicate listname)
  if(NOT "${ARGN}" STREQUAL "")
    if(${listname})
      list(REMOVE_ITEM ${listname} ${ARGN})
    endif()
    list(APPEND ${listname} ${ARGN})
  endif()
endmacro()

# append elements to a list if they are not already in the list
# copied from catkin/cmake/list_append_unique.cmake to keep pkgConfig
# self contained
macro(_list_append_unique listname)
  foreach(_item ${ARGN})
    list(FIND ${listname} ${_item} _index)
    if(_index EQUAL -1)
      list(APPEND ${listname} ${_item})
    endif()
  endforeach()
endmacro()

# pack a list of libraries with optional build configuration keywords
# copied from catkin/cmake/catkin_libraries.cmake to keep pkgConfig
# self contained
macro(_pack_libraries_with_build_configuration VAR)
  set(${VAR} "")
  set(_argn ${ARGN})
  list(LENGTH _argn _count)
  set(_index 0)
  while(${_index} LESS ${_count})
    list(GET _argn ${_index} lib)
    if("${lib}" MATCHES "^(debug|optimized|general)$")
      math(EXPR _index "${_index} + 1")
      if(${_index} EQUAL ${_count})
        message(FATAL_ERROR "_pack_libraries_with_build_configuration() the list of libraries '${ARGN}' ends with '${lib}' which is a build configuration keyword and must be followed by a library")
      endif()
      list(GET _argn ${_index} library)
      list(APPEND ${VAR} "${lib}${CATKIN_BUILD_CONFIGURATION_KEYWORD_SEPARATOR}${library}")
    else()
      list(APPEND ${VAR} "${lib}")
    endif()
    math(EXPR _index "${_index} + 1")
  endwhile()
endmacro()

# unpack a list of libraries with optional build configuration keyword prefixes
# copied from catkin/cmake/catkin_libraries.cmake to keep pkgConfig
# self contained
macro(_unpack_libraries_with_build_configuration VAR)
  set(${VAR} "")
  foreach(lib ${ARGN})
    string(REGEX REPLACE "^(debug|optimized|general)${CATKIN_BUILD_CONFIGURATION_KEYWORD_SEPARATOR}(.+)$" "\\1;\\2" lib "${lib}")
    list(APPEND ${VAR} "${lib}")
  endforeach()
endmacro()


if(pcl_conversions_CONFIG_INCLUDED)
  return()
endif()
set(pcl_conversions_CONFIG_INCLUDED TRUE)

# set variables for source/devel/install prefixes
if("TRUE" STREQUAL "TRUE")
  set(pcl_conversions_SOURCE_PREFIX /home/dhruv/ros/self_driving_car/src/perception_pcl-melodic-devel/pcl_conversions)
  set(pcl_conversions_DEVEL_PREFIX /home/dhruv/ros/self_driving_car/devel)
  set(pcl_conversions_INSTALL_PREFIX "")
  set(pcl_conversions_PREFIX ${pcl_conversions_DEVEL_PREFIX})
else()
  set(pcl_conversions_SOURCE_PREFIX "")
  set(pcl_conversions_DEVEL_PREFIX "")
  set(pcl_conversions_INSTALL_PREFIX /home/dhruv/ros/self_driving_car/install)
  set(pcl_conversions_PREFIX ${pcl_conversions_INSTALL_PREFIX})
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "WARNING: package 'pcl_conversions' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  message("${_msg}")
endif()

# flag project as catkin-based to distinguish if a find_package()-ed project is a catkin project
set(pcl_conversions_FOUND_CATKIN_PROJECT TRUE)

if(NOT "/home/dhruv/ros/self_driving_car/src/perception_pcl-melodic-devel/pcl_conversions/include;/usr/include/eigen3;/usr/local/include/pcl-1.9;/usr/include;/usr/include/ni;/usr/include/openni2;/usr/local/include/vtk-8.1 " STREQUAL " ")
  set(pcl_conversions_INCLUDE_DIRS "")
  set(_include_dirs "/home/dhruv/ros/self_driving_car/src/perception_pcl-melodic-devel/pcl_conversions/include;/usr/include/eigen3;/usr/local/include/pcl-1.9;/usr/include;/usr/include/ni;/usr/include/openni2;/usr/local/include/vtk-8.1")
  if(NOT "https://github.com/ros-perception/perception_pcl/issues " STREQUAL " ")
    set(_report "Check the issue tracker 'https://github.com/ros-perception/perception_pcl/issues' and consider creating a ticket if the problem has not been reported yet.")
  elseif(NOT "http://wiki.ros.org/pcl_conversions " STREQUAL " ")
    set(_report "Check the website 'http://wiki.ros.org/pcl_conversions' for information and consider reporting the problem.")
  else()
    set(_report "Report the problem to the maintainer 'Paul Bovbel <paul@bovbel.com>, Kentaro Wada <www.kentaro.wada@gmail.com>' and request to fix the problem.")
  endif()
  foreach(idir ${_include_dirs})
    if(IS_ABSOLUTE ${idir} AND IS_DIRECTORY ${idir})
      set(include ${idir})
    elseif("${idir} " STREQUAL "include ")
      get_filename_component(include "${pcl_conversions_DIR}/../../../include" ABSOLUTE)
      if(NOT IS_DIRECTORY ${include})
        message(FATAL_ERROR "Project 'pcl_conversions' specifies '${idir}' as an include dir, which is not found.  It does not exist in '${include}'.  ${_report}")
      endif()
    else()
      message(FATAL_ERROR "Project 'pcl_conversions' specifies '${idir}' as an include dir, which is not found.  It does neither exist as an absolute directory nor in '/home/dhruv/ros/self_driving_car/src/perception_pcl-melodic-devel/pcl_conversions/${idir}'.  ${_report}")
    endif()
    _list_append_unique(pcl_conversions_INCLUDE_DIRS ${include})
  endforeach()
endif()

set(libraries "/usr/local/lib/libpcl_common.so;/usr/local/lib/libpcl_octree.so;/usr/local/lib/libpcl_io.so;/usr/lib/x86_64-linux-gnu/libboost_system.so;/usr/lib/x86_64-linux-gnu/libboost_filesystem.so;/usr/lib/x86_64-linux-gnu/libboost_thread.so;/usr/lib/x86_64-linux-gnu/libboost_date_time.so;/usr/lib/x86_64-linux-gnu/libboost_iostreams.so;/usr/lib/x86_64-linux-gnu/libboost_serialization.so;/usr/lib/x86_64-linux-gnu/libboost_chrono.so;/usr/lib/x86_64-linux-gnu/libboost_atomic.so;/usr/lib/x86_64-linux-gnu/libboost_regex.so;/usr/lib/x86_64-linux-gnu/libpthread.so;/usr/lib/libOpenNI.so;/usr/lib/libOpenNI2.so;/usr/local/lib/libvtksys-8.1.so.1;/usr/local/lib/libvtkCommonCore-8.1.so.1;/usr/local/lib/libvtkCommonMath-8.1.so.1;/usr/local/lib/libvtkCommonMisc-8.1.so.1;/usr/local/lib/libvtkCommonSystem-8.1.so.1;/usr/local/lib/libvtkCommonTransforms-8.1.so.1;/usr/local/lib/libvtkCommonDataModel-8.1.so.1;/usr/local/lib/libvtkCommonColor-8.1.so.1;/usr/local/lib/libvtkCommonExecutionModel-8.1.so.1;/usr/local/lib/libvtkCommonComputationalGeometry-8.1.so.1;/usr/local/lib/libvtkFiltersCore-8.1.so.1;/usr/local/lib/libvtkFiltersGeneral-8.1.so.1;/usr/local/lib/libvtkImagingCore-8.1.so.1;/usr/local/lib/libvtkImagingFourier-8.1.so.1;/usr/local/lib/libvtkalglib-8.1.so.1;/usr/local/lib/libvtkFiltersStatistics-8.1.so.1;/usr/local/lib/libvtkFiltersExtraction-8.1.so.1;/usr/local/lib/libvtkInfovisCore-8.1.so.1;/usr/local/lib/libvtkFiltersGeometry-8.1.so.1;/usr/local/lib/libvtkFiltersSources-8.1.so.1;/usr/local/lib/libvtkRenderingCore-8.1.so.1;/usr/local/lib/libvtkzlib-8.1.so.1;/usr/local/lib/libvtkfreetype-8.1.so.1;/usr/local/lib/libvtkRenderingFreeType-8.1.so.1;/usr/local/lib/libvtkRenderingContext2D-8.1.so.1;/usr/local/lib/libvtkChartsCore-8.1.so.1;/usr/local/lib/libvtkDICOMParser-8.1.so.1;/usr/local/lib/libvtklz4-8.1.so.1;/usr/local/lib/libvtkIOCore-8.1.so.1;/usr/local/lib/libvtkIOLegacy-8.1.so.1;/usr/local/lib/libvtkexpat-8.1.so.1;/usr/local/lib/libvtkIOXMLParser-8.1.so.1;/usr/local/lib/libvtkDomainsChemistry-8.1.so.1;/usr/local/lib/libvtkglew-8.1.so.1;/usr/local/lib/libvtkRenderingOpenGL2-8.1.so.1;/usr/local/lib/libvtkDomainsChemistryOpenGL2-8.1.so.1;/usr/local/lib/libvtkIOXML-8.1.so.1;/usr/local/lib/libvtkParallelCore-8.1.so.1;/usr/local/lib/libvtkFiltersAMR-8.1.so.1;/usr/local/lib/libvtkFiltersFlowPaths-8.1.so.1;/usr/local/lib/libvtkFiltersGeneric-8.1.so.1;/usr/local/lib/libvtkImagingSources-8.1.so.1;/usr/local/lib/libvtkFiltersHybrid-8.1.so.1;/usr/local/lib/libvtkFiltersHyperTree-8.1.so.1;/usr/local/lib/libvtkImagingGeneral-8.1.so.1;/usr/local/lib/libvtkFiltersImaging-8.1.so.1;/usr/local/lib/libvtkFiltersModeling-8.1.so.1;/usr/local/lib/libvtkFiltersParallel-8.1.so.1;/usr/local/lib/libvtkFiltersParallelImaging-8.1.so.1;/usr/local/lib/libvtkFiltersPoints-8.1.so.1;/usr/local/lib/libvtkFiltersProgrammable-8.1.so.1;/usr/local/lib/libvtkFiltersSMP-8.1.so.1;/usr/local/lib/libvtkFiltersSelection-8.1.so.1;/usr/local/lib/libvtkFiltersTexture-8.1.so.1;/usr/local/lib/libvtkFiltersTopology-8.1.so.1;/usr/local/lib/libvtkverdict-8.1.so.1;/usr/local/lib/libvtkFiltersVerdict-8.1.so.1;/usr/local/lib/libvtkmetaio-8.1.so.1;/usr/local/lib/libvtkjpeg-8.1.so.1;/usr/local/lib/libvtkpng-8.1.so.1;/usr/local/lib/libvtktiff-8.1.so.1;/usr/local/lib/libvtkIOImage-8.1.so.1;/usr/local/lib/libvtkImagingHybrid-8.1.so.1;/usr/local/lib/libvtkInfovisLayout-8.1.so.1;/usr/local/lib/libvtkInteractionStyle-8.1.so.1;/usr/local/lib/libvtkImagingColor-8.1.so.1;/usr/local/lib/libvtkRenderingAnnotation-8.1.so.1;/usr/local/lib/libvtkRenderingVolume-8.1.so.1;/usr/local/lib/libvtkInteractionWidgets-8.1.so.1;/usr/local/lib/libvtkViewsCore-8.1.so.1;/usr/local/lib/libvtkproj4-8.1.so.1;/usr/local/lib/libvtkGeovisCore-8.1.so.1;/usr/local/lib/libvtkhdf5_hl-8.1.so.1;/usr/local/lib/libvtkhdf5-8.1.so.1;/usr/local/lib/libvtkIOAMR-8.1.so.1;/usr/local/lib/libvtkIOEnSight-8.1.so.1;/usr/local/lib/libvtkNetCDF-8.1.so.1;/usr/local/lib/libvtkexoIIc-8.1.so.1;/usr/local/lib/libvtkIOExodus-8.1.so.1;/usr/local/lib/libvtkgl2ps-8.1.so.1;/usr/local/lib/libvtkRenderingGL2PSOpenGL2-8.1.so.1;/usr/local/lib/libvtklibharu-8.1.so.1;/usr/local/lib/libvtkIOExport-8.1.so.1;/usr/local/lib/libvtkIOExportOpenGL2-8.1.so.1;/usr/local/lib/libvtkIOGeometry-8.1.so.1;/usr/local/lib/libvtkIOImport-8.1.so.1;/usr/local/lib/libvtklibxml2-8.1.so.1;/usr/local/lib/libvtkIOInfovis-8.1.so.1;/usr/local/lib/libvtkIOLSDyna-8.1.so.1;/usr/local/lib/libvtkIOMINC-8.1.so.1;/usr/local/lib/libvtkoggtheora-8.1.so.1;/usr/local/lib/libvtkIOMovie-8.1.so.1;/usr/local/lib/libvtknetcdfcpp-8.1.so.1;/usr/local/lib/libvtkIONetCDF-8.1.so.1;/usr/local/lib/libvtkIOPLY-8.1.so.1;/usr/local/lib/libvtkjsoncpp-8.1.so.1;/usr/local/lib/libvtkIOParallel-8.1.so.1;/usr/local/lib/libvtkIOParallelXML-8.1.so.1;/usr/local/lib/libvtksqlite-8.1.so.1;/usr/local/lib/libvtkIOSQL-8.1.so.1;/usr/local/lib/libvtkIOTecplotTable-8.1.so.1;/usr/local/lib/libvtkIOVideo-8.1.so.1;/usr/local/lib/libvtkImagingMath-8.1.so.1;/usr/local/lib/libvtkImagingMorphological-8.1.so.1;/usr/local/lib/libvtkImagingStatistics-8.1.so.1;/usr/local/lib/libvtkImagingStencil-8.1.so.1;/usr/local/lib/libvtkInteractionImage-8.1.so.1;/usr/local/lib/libvtkRenderingContextOpenGL2-8.1.so.1;/usr/local/lib/libvtkRenderingImage-8.1.so.1;/usr/local/lib/libvtkRenderingLOD-8.1.so.1;/usr/local/lib/libvtkRenderingLabel-8.1.so.1;/usr/local/lib/libvtkRenderingVolumeOpenGL2-8.1.so.1;/usr/local/lib/libvtkViewsContext2D-8.1.so.1;/usr/local/lib/libvtkViewsInfovis-8.1.so.1")
foreach(library ${libraries})
  # keep build configuration keywords, target names and absolute libraries as-is
  if("${library}" MATCHES "^(debug|optimized|general)$")
    list(APPEND pcl_conversions_LIBRARIES ${library})
  elseif(${library} MATCHES "^-l")
    list(APPEND pcl_conversions_LIBRARIES ${library})
  elseif(TARGET ${library})
    list(APPEND pcl_conversions_LIBRARIES ${library})
  elseif(IS_ABSOLUTE ${library})
    list(APPEND pcl_conversions_LIBRARIES ${library})
  else()
    set(lib_path "")
    set(lib "${library}-NOTFOUND")
    # since the path where the library is found is returned we have to iterate over the paths manually
    foreach(path /home/dhruv/ros/self_driving_car/devel/lib;/home/dhruv/ros/self_driving_car/devel/lib;/opt/ros/melodic/lib)
      find_library(lib ${library}
        PATHS ${path}
        NO_DEFAULT_PATH NO_CMAKE_FIND_ROOT_PATH)
      if(lib)
        set(lib_path ${path})
        break()
      endif()
    endforeach()
    if(lib)
      _list_append_unique(pcl_conversions_LIBRARY_DIRS ${lib_path})
      list(APPEND pcl_conversions_LIBRARIES ${lib})
    else()
      # as a fall back for non-catkin libraries try to search globally
      find_library(lib ${library})
      if(NOT lib)
        message(FATAL_ERROR "Project '${PROJECT_NAME}' tried to find library '${library}'.  The library is neither a target nor built/installed properly.  Did you compile project 'pcl_conversions'?  Did you find_package() it before the subdirectory containing its code is included?")
      endif()
      list(APPEND pcl_conversions_LIBRARIES ${lib})
    endif()
  endif()
endforeach()

set(pcl_conversions_EXPORTED_TARGETS "")
# create dummy targets for exported code generation targets to make life of users easier
foreach(t ${pcl_conversions_EXPORTED_TARGETS})
  if(NOT TARGET ${t})
    add_custom_target(${t})
  endif()
endforeach()

set(depends "pcl_msgs;roscpp;sensor_msgs;std_msgs")
foreach(depend ${depends})
  string(REPLACE " " ";" depend_list ${depend})
  # the package name of the dependency must be kept in a unique variable so that it is not overwritten in recursive calls
  list(GET depend_list 0 pcl_conversions_dep)
  list(LENGTH depend_list count)
  if(${count} EQUAL 1)
    # simple dependencies must only be find_package()-ed once
    if(NOT ${pcl_conversions_dep}_FOUND)
      find_package(${pcl_conversions_dep} REQUIRED NO_MODULE)
    endif()
  else()
    # dependencies with components must be find_package()-ed again
    list(REMOVE_AT depend_list 0)
    find_package(${pcl_conversions_dep} REQUIRED NO_MODULE ${depend_list})
  endif()
  _list_append_unique(pcl_conversions_INCLUDE_DIRS ${${pcl_conversions_dep}_INCLUDE_DIRS})

  # merge build configuration keywords with library names to correctly deduplicate
  _pack_libraries_with_build_configuration(pcl_conversions_LIBRARIES ${pcl_conversions_LIBRARIES})
  _pack_libraries_with_build_configuration(_libraries ${${pcl_conversions_dep}_LIBRARIES})
  _list_append_deduplicate(pcl_conversions_LIBRARIES ${_libraries})
  # undo build configuration keyword merging after deduplication
  _unpack_libraries_with_build_configuration(pcl_conversions_LIBRARIES ${pcl_conversions_LIBRARIES})

  _list_append_unique(pcl_conversions_LIBRARY_DIRS ${${pcl_conversions_dep}_LIBRARY_DIRS})
  list(APPEND pcl_conversions_EXPORTED_TARGETS ${${pcl_conversions_dep}_EXPORTED_TARGETS})
endforeach()

set(pkg_cfg_extras "")
foreach(extra ${pkg_cfg_extras})
  if(NOT IS_ABSOLUTE ${extra})
    set(extra ${pcl_conversions_DIR}/${extra})
  endif()
  include(${extra})
endforeach()
