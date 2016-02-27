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
import qbs.FileInfo
import Stoiridh.Cpp

Cpp.BaseProduct {
    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Dependencies                                                                              //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Depends { name: 'Qt'; submodules: ['core', 'gui', 'qml', 'quick'] }

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Configuration                                                                             //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    property stringList qmlImportPaths: FileInfo.joinPaths(qbs.installRoot, project.qmlDirectory)

    Qt.quick.qmlDebugging: qbs.buildVariant === 'debug'
    Qt.quick.qmlImportsPath: FileInfo.joinPaths(qbs.installRoot, project.qmlDirectory)
}
