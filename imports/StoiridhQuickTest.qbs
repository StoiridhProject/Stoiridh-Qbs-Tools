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

StoiridhQuickProduct {
    type: ["application", "autotest", "qtquick-test"]
    targetName: "tst_" + testName

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Properties                                                                                //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    property string testName: ""

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Dependencies                                                                              //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Depends { name: "Qt"; submodules: ["testlib", "quicktest"] }

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Configuration                                                                             //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Qt.quicktest.sourceDirectory: FileInfo.joinPaths(product.sourceDirectory, "qml")

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  QML                                                                                       //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Group {
        name: "QML"
        prefix: "qml/"
        files: "*.qml"
        fileTags: ["qml"]
    }
    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Rules                                                                                     //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Rule {
        inputs: ['qml']

        Artifact {
            filePath: FileInfo.joinPaths("qml", input.fileName)
            fileTags: ['qtquick-test']
        }

        prepare: {
            var cmd = new JavaScriptCommand();
            cmd.silent = true;
            cmd.sourceCode = function() { File.copy(input.filePath, output.filePath); };
            return cmd;
        }
    }
}
