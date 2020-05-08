#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import platform
from conans import ConanFile, tools


class JavaInstallerConan(ConanFile):
    name = 'java_installer'
    version = '8.0.252'
    url = 'https://github.com/bincrafters/conan-java_installer'
    description = 'Java installer distributed via Conan'
    license = 'https://www.azul.com/products/zulu-and-zulu-enterprise/zulu-terms-of-use/'
    settings = 'os', 'arch'

    @property
    def jni_folder(self):
        folder = {'Linux': 'linux', 'Darwin': 'darwin',
                  'Windows': 'win32'}.get(platform.system())
        return os.path.join('include', folder)

    def config_options(self):
        # Checking against self.settings.* would prevent cross-building profiles from working
        if self.settings.arch not in ['x86_64', 'x86']:
            raise Exception(
                'Unsupported Architecture.  This package currently only supports x86_64 and x86.')
        if self.settings.os not in ['Windows', 'Macos', 'Linux']:
            raise Exception(
                'Unsupported System. This package currently only support Linux/Darwin/Windows')
        if self.settings.os == 'Macos' and self.settings.arch == 'x86':
            raise Exception('Unsupported System (32-bit Mac OS X)')

    def build(self):
        x64 = self.settings.arch == 'x86_64'
        source_file = 'zulu8.{0}-ca-jdk{1}-{2}_{3}'
        zulu_version = '46.0.19'
        ext = 'tar.gz'
        arch = 'x64' if x64 else 'i686'
        if self.settings.os == 'Windows':
            source_file = source_file.format(
                zulu_version, self.version, 'win', arch)
            ext = 'zip'
            if x64:
                checksum = '993ef31276d18446ef8b0c249b40aa2dfcea221a5725d9466cbea1ba22686f6b'
            else:
                checksum = '44fa7abc0f647a014b2c6a6cf78000cc2a554b15132ea83e60229ea58a77c551'
        elif self.settings.os == 'Linux':
            source_file = source_file.format(
                zulu_version, self.version, 'linux', arch)
            if x64:
                checksum = 'ab8a4194006f12dd48bf7f176ca7879706d3f8fc7d3208313a46cc9ee2270716'
            else:
                checksum = 'bba0ec1606823515172e3eee9fcaa9ea29d51be49ee903c4b1e708af3e60a29f'
        elif self.settings.os == 'Macos':
            source_file = source_file.format(
                zulu_version, self.version, 'macosx', arch)
            checksum = '43570b0a6455a02d25b0c4937164560fdb0a9478f9010c583f510fa80881ce0b'

        bin_filename = '{0}.{1}'.format(source_file, ext)
        download_url = 'http://cdn.azul.com/zulu/bin/{0}'.format(bin_filename)
        self.output.info('Downloading : {0}'.format(download_url))
        tools.get(download_url, sha256=checksum)
        os.rename(source_file, 'sources')

    def package(self):
        self.copy(pattern='*', dst='.', src='sources')

    def package_info(self):
        self.cpp_info.includedirs.append(self.jni_folder)

        java_home = os.path.join(self.package_folder)
        bin_path = os.path.join(java_home, 'bin')

        self.output.info(
            'Creating JAVA_HOME environment variable with : {0}'.format(java_home))
        self.env_info.JAVA_HOME = java_home

        self.output.info(
            'Appending PATH environment variable with : {0}'.format(bin_path))
        self.env_info.PATH.append(bin_path)
