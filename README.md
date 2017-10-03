## This repository holds a conan recipe for Java. 

[![Appveyor Status](https://ci.appveyor.com/api/projects/status/fgsifwucqj8fo5pm/branch/stable/9.0.0?svg=true)](https://ci.appveyor.com/project/BinCrafters/conan-java-installer/branch/stable/9.0.0)
[![Travis Status](https://travis-ci.org/bincrafters/conan-java_installer.svg?branch=stable%2F9.0.0)](https://travis-ci.org/bincrafters/conan-java_installer)

[Conan.io](https://conan.io) package for [Java](https://www.azul.com/downloads/zulu) project

The packages generated with this **conanfile** can be found in [Bintray](https://bintray.com/bincrafters/public-conan/java_installer%3Abincrafters).

This Conan package contains the Java Development Kit (JDK).  It is cross platform and is intended to be used as a Conan "`build_requirement`" for C++ projects which require Java to be built.  Google's build system "Bazel" is one example of a C++ build system which requires Java.  Note that this package should not interfere or interact with other installations of Java on the machine.  It does not change any persistent environment variables, it only adds/modifies those for the existing process.  It passes the required environment variables to packages which list it as a `requirement` or `build_requirement` via Conan's native `env_info` functionality.  

This package is based on Azul Systems' Zulu build of OpenJDK.  It's a certified and stable build that and functionally equivalent to Oracle's (as well as IBM's, Redhat's, and other certified builds).  There are a number of advantages to using Zulu, which have caused many projects and organizations to use it as the default, including Microsoft Azure. If you are unfamilliar but interested in the differences between JDK providers, you are encouraged to research the topic. 

## For Users: Use this package

### Basic setup

    $ conan install java_installer/9.0.0@bincrafters/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    java_installer/9.0.0@bincrafters/stable

    [generators]
    txt

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..
	
Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git. 

## For Packagers: Publish this Package

The example below shows the commands used to publish to bincrafters conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly. 

## Create and Package 

The following command both runs all the steps of the conan file, and publishes the package to the local system cache. 

    $ conan create bincrafters/stable
	
## Add Remote

	$ conan remote add bincrafters "https://api.bintray.com/conan/bincrafters/public-conan"

## Upload

    $ conan upload java_installer/9.0.0@bincrafters/stable --all -r bincrafters

	
## License
[Zulu License](https://www.azul.com/products/zulu-and-zulu-enterprise/zulu-terms-of-use)
