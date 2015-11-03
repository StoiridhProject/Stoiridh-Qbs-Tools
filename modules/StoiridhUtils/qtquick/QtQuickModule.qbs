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
    name: "qtquick"

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Properties                                                                                //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    property string uri
    property string qmlDir
    property string installDir

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  FileTagger                                                                                //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    FileTagger {
        fileTags: 'qml'
        patterns: ['*.qml', 'qmldir']
    }
    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Validate                                                                                  //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    validate: {
        var validator = new ModUtils.PropertyValidator("qtquick");
        validator.setRequiredProperty("uri", uri);
        validator.setRequiredProperty("qmlDir", qmlDir);
        validator.setRequiredProperty("installDir", installDir);
        validator.validate();
    }
    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Rules                                                                                     //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Rule {
        inputs: ['qml']

        outputArtifacts: {
            var qmlDir = ModUtils.moduleProperty(product, "qmlDir");
            var qmlPath = FileInfo.joinPaths(product.sourceDirectory, qmlDir);
            var installDir = ModUtils.moduleProperty(product, "installDir");
            var path = FileInfo.joinPaths(installDir, FileInfo.relativePath(qmlPath, input.filePath));

            return [{fileTags: ['qtquick-plugin'], filePath: path}];
        }
        outputFileTags: ['qtquick-plugin']

        prepare: {
            var uri = ModUtils.moduleProperty(product, "uri");
            var cmd = new JavaScriptCommand();
            cmd.description = "[" + uri + "] copying " + input.fileName;
            cmd.sourceCode = function() {
                File.copy(input.filePath, output.filePath);
            };
            return cmd;
        }
    }
}
