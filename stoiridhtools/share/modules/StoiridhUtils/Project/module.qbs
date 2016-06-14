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
import Stoiridh.Utils

Module {
    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Properties                                                                                //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    property string productName: undefined

    property string binaryDirectory: {
        return Utils.getProperty(project.binaryDirectory, 'bin');
    }

    property string librariesDirectory: {
        return Utils.getProperty(project.librariesDirectory, 'lib');
    }

    property string pluginsDirectory: {
        var pluginsDirectory = FileInfo.joinPaths(librariesDirectory, productName, 'plugins');
        return Utils.getProperty(project.pluginsDirectory, pluginsDirectory);
    }

    property string qmlDirectory: {
        var qmlDirectory = FileInfo.joinPaths(librariesDirectory, productName, 'qml');
        return Utils.getProperty(project.qmlDirectory, qmlDirectory);
    }

    property string shareDirectory: {
        var shareDirectory = FileInfo.joinPaths('share', productName);
        return Utils.getProperty(project.shareDirectory, shareDirectory);
    }

    property string docDirectory: {
        var docDirectory = FileInfo.joinPaths('share', 'doc', productName);
        return Utils.getProperty(project.docDirectory, docDirectory);
    }
}
