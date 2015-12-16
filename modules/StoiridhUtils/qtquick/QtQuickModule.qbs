////////////////////////////////////////////////////////////////////////////////////////////////////
//                                                                                                //
//            Copyright (C) 2015 William McKIE                                                    //
//                                                                                                //
//            This program is free software: you can redistribute it and/or modify                //
//            it under the terms of the GNU General Public License as published by                //
//            the Free Software Foundation, either version 3 of the License, or                   //
//            (at your option) any later version.                                                 //
//                                                                                                //
//            This program is distributed in the hope that it will be useful,                     //
//            but WITHOUT ANY WARRANTY; without even the implied warranty of                      //
//            MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                       //
//            GNU General Public License for more details.                                        //
//                                                                                                //
//            You should have received a copy of the GNU General Public License                   //
//            along with this program.  If not, see <http://www.gnu.org/licenses/>.               //
//                                                                                                //
////////////////////////////////////////////////////////////////////////////////////////////////////
import qbs 1.0
import qbs.File
import qbs.FileInfo
import qbs.ModUtils

Module {
    name: 'qtquick'
    additionalProductTypes: ['copied_qml_files', 'copied_qmldir_files']

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Properties                                                                                //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    property string uri
    property string importVersion
    property string qmlSourceDirectory
    property string installDirectory

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  FileTagger                                                                                //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    FileTagger {
        fileTags: 'qml'
        patterns: ['*.qml']
    }

    FileTagger {
        fileTags: 'qmldir'
        patterns: ['qmldir']
    }
    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Validate                                                                                  //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    validate: {
        var validator = new ModUtils.PropertyValidator('qtquick');
        validator.setRequiredProperty('uri', uri);
        validator.setRequiredProperty('importVersion', importVersion);
        validator.setRequiredProperty('qmlSourceDirectory', qmlSourceDirectory);
        validator.setRequiredProperty('installDirectory', installDirectory);
        validator.validate();
    }
    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Rules                                                                                     //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Rule {
        inputs: ['qml', 'qmldir']

        outputFileTags: ['copied_qml_files', 'copied_qmldir_files']
        outputArtifacts: {
            var uri = ModUtils.moduleProperty(product, 'uri');
            var qmlSourceDirectory = ModUtils.moduleProperty(product, 'qmlSourceDirectory');
            var installDirectory = FileInfo.joinPaths(ModUtils.moduleProperty(product, 'installDirectory'),
                                                      uri.replace(/\./g, '/'));
            var filePath = FileInfo.joinPaths(installDirectory, FileInfo.relativePath(qmlSourceDirectory,
                                                                                input.filePath));
            var artifacts = [];

            if (input.fileTags.contains('qmldir')) {
                artifacts.push({ filePath: filePath, fileTags: ['copied_qmldir_files'] });
            } else {
                artifacts.push({ filePath: filePath, fileTags: ['copied_qml_files'] });
            }

            return artifacts;
        }

        prepare: {
            var uri = ModUtils.moduleProperty(product, 'uri');
            var qmlSourceDirectory = ModUtils.moduleProperty(product, 'qmlSourceDirectory');
            var subdirectory = FileInfo.path(FileInfo.relativePath(qmlSourceDirectory,
                                                                   input.filePath));

            if (subdirectory !== '.')
                uri += '.' + subdirectory;

            var cmd = new JavaScriptCommand();
            cmd.description = '[' + uri + '] copying ' + input.fileName;
            cmd.sourceCode = function() {
                File.copy(input.filePath, output.filePath)
            };

            return cmd;
        }
    }
}
