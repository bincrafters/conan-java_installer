from conans import ConanFile, tools
from conans.tools import os_info
import os


class JavaInstallerConan(ConanFile):
    name = "java_installer"
    version = "9.0.0"
    url = "https://github.com/bincrafters/conan-java_installer"
    description = "Java installer distributed via Conan"
    license = "https://www.azul.com/products/zulu-and-zulu-enterprise/zulu-terms-of-use/"
    settings = "os", "arch"

    @property
    def jni_folder(self):
        if os_info.is_windows:
            folder = "win32"
        elif os_info.is_macos:
            folder = "darwin"
        elif os_info.is_linux:
            folder = "linux"
        else:
            raise Exception("Unsupported System. This package currently only support Linux/Darwin/Windows")
        return os.path.join("include", folder)

    def config_options(self):
        if self.settings.arch != "x86_64":
            raise Exception("Unsupported Architecture.  This package currently only supports x86_64.")

    def build(self):
        source_file = "zulu9.0.0.15-jdk{0}-{1}_x64"

        if os_info.is_windows:
            source_file = source_file.format(self.version, "win")
            ext = "zip"
            checksum = "f22d7ee4c277e0bf84ecb7cd03dfb13f"
        if os_info.is_linux:
            source_file = source_file.format(self.version, "linux")
            ext = "tar.gz"
            checksum = "de913f2aa03c341d865dfb6a1698f31b"
        if os_info.is_macos:
            source_file = source_file.format(self.version, "macosx")
            ext = "tar.gz"
            checksum = "b99e113f29fc0fad71b696d099e93366"

        bin_filename = "{0}.{1}".format(source_file, ext)
        download_url = "http://cdn.azul.com/zulu/bin/{0}".format(bin_filename)
        self.output.info("Downloading : {0}".format(download_url))
        tools.download(download_url, bin_filename)
        tools.check_md5(bin_filename, checksum)
        tools.unzip(bin_filename)
        os.unlink(bin_filename)
        os.rename(source_file, "java")

    def package(self):
        self.copy(pattern="*", dst=".", src="java")

    def package_info(self):
        bin_path = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable with : {0}".format(bin_path))
        self.env_info.path.append(bin_path)

        # do not forget to add the platform-specific JNI folder
        self.cpp_info.includedirs.append(self.jni_folder)
        self.output.info("Creating JAVA_HOME environment variable with : {0}".format(bin_path))
        self.env_info.JAVA_HOME = os.path.join(self.package_folder)
