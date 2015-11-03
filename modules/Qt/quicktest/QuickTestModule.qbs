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
import qbs.FileInfo

Module {
    id: quicktest

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Properties                                                                                //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    property string sourceDirectory

    readonly property stringList __quiktestDefines: [
        "QT_QMLTEST_LIB"
    ].concat(sourceDirectory !== "" ? ['QUICK_TEST_SOURCE_DIR="' + sourceDirectory + '"']
                                    : [])

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Dependencies                                                                              //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Depends { name: "cpp" }
    Depends { name: "Qt.core" }

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Configuration                                                                             //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    cpp.dynamicLibraries: "Qt5QuickTest"
    cpp.defines: __quiktestDefines
    cpp.includePaths: FileInfo.joinPaths(Qt.core.incPath, "QtQuickTest")

    Qt.core.config: ["warn_on", "qmltestcase"]
}
