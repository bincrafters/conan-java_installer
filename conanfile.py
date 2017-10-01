from conans import ConanFile, tools, os
from conans.tools import os_info


class JavaConan(ConanFile):
    name = "Java"
    version = "8.0.144"
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/bincrafters/conan-java"
    description = "Java installer distributed via Conan"
    license = "https://www.azul.com/products/zulu-and-zulu-enterprise/zulu-terms-of-use/"
    
    def source(self):
        source_file = "zulu8.23.0.3-jdk{0}-{1}_x64"
        ext = ""
        if os_info.is_windows:
            source_file = source_file.format(self.version, "win")
            ext = "zip"
        if os_info.is_linux:
            source_file = source_file.format(self.version, "linux")
            ext = "tar.gz"
        if os_info.is_macos:
            source_file = source_file.format(self.version, "macosx")
            ext = "tar.gz"
        tools.get("http://cdn.azul.com/zulu/bin/{0}.{1}".format(source_file, ext))
        os.rename(source_file, "java")
            
    def build(self):
        pass            
                    
    def package(self):
        self.copy(pattern="*", dst=".", src="java")

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))