#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os
import platform


class JavaInstallerConan(ConanFile):
    name = "java_installer"
    # x86 is 8.0.153, while x86_64 is 8.0.152
    version = "8.0.153"
    url = "https://github.com/bincrafters/conan-java_installer"
    description = "Java installer distributed via Conan"
    license = "https://www.azul.com/products/zulu-and-zulu-enterprise/zulu-terms-of-use/"
    settings = "os_build", "arch_build"

    @property
    def jni_folder(self):
        folder = {"Linux": "linux", "Darwin": "darwin", "Windows": "win32"}.get(platform.system())
        return os.path.join("include", folder)

    def config_options(self):
        # Checking against self.settings.* would prevent cross-building profiles from working
        if self.settings.arch_build not in ["x86_64", "x86"]:
            raise Exception("Unsupported Architecture.  This package currently only supports x86_64 and x86.")
        if self.settings.os_build not in ["Windows", "Macos", "Linux"]:
            raise Exception("Unsupported System. This package currently only support Linux/Darwin/Windows")
        if self.settings.os_build == "Macos" and self.settings.arch_build == "x86":
            raise Exception("Unsupported System (32-bit Mac OS X)")

    def build(self):
        x64 = self.settings.arch_build == 'x86_64'
        source_file = "zulu8.{0}-jdk{1}-{2}_{3}"
        zulu_version = '25.0.1' if x64 else '25.0.3'
        version = '8.0.152' if x64 else '8.0.153'
        arch = 'x64' if x64 else 'i686'

        if self.settings.os_build == 'Windows':
            source_file = source_file.format(zulu_version, version, "win", arch)
            ext = "zip"
            checksum = "754bd10d29212c817dfad8758a8df9bc" if x64 else "67752bd3cb8356215900883b55a8c26c"
        elif self.settings.os_build == 'Linux':
            source_file = source_file.format(zulu_version, version, "linux", arch)
            ext = "tar.gz"
            checksum = "cc6e9ff13c27d27033220208d5450f2d" if x64 else "99da96ba61ccb53aab85261d4746b51c"
        elif self.settings.os_build == 'Macos':
            source_file = source_file.format(zulu_version, version, "macosx", arch)
            ext = "tar.gz"
            checksum = "0348962b47bf5197e7b5e78cfd073d84"

        bin_filename = "{0}.{1}".format(source_file, ext)
        download_url = "http://cdn.azul.com/zulu/bin/{0}".format(bin_filename)
        self.output.info("Downloading : {0}".format(download_url))
        tools.get(download_url, md5=checksum)
        os.rename(source_file, "sources")

    def package(self):
        self.copy(pattern="*", dst=".", src="sources")

    def package_info(self):
        self.cpp_info.includedirs.append(self.jni_folder)

        java_home = os.path.join(self.package_folder)
        bin_path = os.path.join(java_home, "bin")

        self.output.info("Creating JAVA_HOME environment variable with : {0}".format(java_home))
        self.env_info.JAVA_HOME = java_home
        
        self.output.info("Appending PATH environment variable with : {0}".format(bin_path))
        self.env_info.path.append(bin_path)
