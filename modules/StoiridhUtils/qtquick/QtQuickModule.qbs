////////////////////////////////////////////////////////////////////////////////////////////////////
//                                                                                                //
//            Copyright (C) 2015-2016 William McKIE                                               //
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
    additionalProductTypes: ['qml-data']

    Properties {
        condition: (!qbs.hostOS.contains('windows')
                    || (qbs.hostOS.contains('windows') && qbs.buildVariant === 'release'))
        additionalProductTypes: outer.concat(['stoiridh-internal-python-process'])
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Dependencies                                                                              //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Depends {
        id: python
        condition: (!qbs.hostOS.contains('windows')
                    || (qbs.hostOS.contains('windows') && qbs.buildVariant === 'release'))
        name: 'Python'
        required: true
    }
    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Properties                                                                                //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    property string uri
    property string importVersion
    property string qmlSourceDirectory
    property string installDirectory

    /*! \internal */
    property path pythonModuleFilePath

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Validate                                                                                  //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    validate: {
        var validator = new ModUtils.PropertyValidator('qtquick');
        validator.setRequiredProperty('uri', uri);
        validator.setRequiredProperty('importVersion', importVersion);
        validator.setRequiredProperty('qmlSourceDirectory', qmlSourceDirectory);
        validator.setRequiredProperty('installDirectory', installDirectory);
        validator.setRequiredProperty('pythonModuleFilePath', pythonModuleFilePath);
        validator.validate();
    }
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

    FileTagger {
        fileTags: 'qmltypes'
        patterns: ['*.qmltypes']
    }
    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Rules                                                                                     //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Rule {
        inputs: ['qml', 'qmldir', 'qmltypes']

        Artifact {
            fileTags: ['qml-data']
            filePath: {
                var uri = ModUtils.moduleProperty(product, 'uri');
                var qmlSourceDirectory = ModUtils.moduleProperty(product, 'qmlSourceDirectory');
                var id = ModUtils.moduleProperty(product, 'installDirectory');
                var installDirectory = FileInfo.joinPaths(id, uri.replace(/\./g, '/'));
                var irfp = FileInfo.relativePath(qmlSourceDirectory, input.filePath);

                return FileInfo.joinPaths(installDirectory, irfp);
            }
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
                File.copy(input.filePath, output.filePath);
            };

            return cmd;
        }
    }

    Rule {
        condition: python.found && python.condition
        inputs: ['qml-data']

        Artifact {
            fileTags: ['stoiridh-internal-python-process']
            filePath: '.deps'
            alwaysUpdated: false
        }

        prepare: {
            var python = product.moduleProperty('Python', 'filePath');
            var script = ModUtils.moduleProperty(product, 'pythonModuleFilePath');

            // arguments
            var qtBinPath = product.moduleProperty('Qt.core', 'binPath');
            var uri = ModUtils.moduleProperty(product, 'uri');
            var importVersion = ModUtils.moduleProperty(product, 'importVersion');
            var id = ModUtils.moduleProperty(product, 'installDirectory');
            var installDirectory = FileInfo.joinPaths(id, uri.replace(/\./g, '/'));

            var args = [script, 'dump', '--qtbindir', qtBinPath, uri, importVersion,
                        installDirectory];

            var cmd = new Command(python, args);
            cmd.silent = true;
            cmd.description = 'running python process for ' + uri;
            cmd.highlight = 'filegen';
            return cmd;
        }
    }
}
