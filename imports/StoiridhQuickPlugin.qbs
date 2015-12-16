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

StoiridhQuickProduct {
    type: ['dynamiclibrary']

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Properties                                                                                //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    property string uri: parent.name
    property string qmlDirectory: 'qml'

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Dependencies                                                                              //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Depends { name: 'StoiridhUtils.qtquick' }

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Configuration                                                                             //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    StoiridhUtils.qtquick.uri: uri
    StoiridhUtils.qtquick.importVersion: version
    StoiridhUtils.qtquick.qmlSourceDirectory: FileInfo.joinPaths(product.sourceDirectory, qmlDirectory)
    StoiridhUtils.qtquick.installDirectory: FileInfo.joinPaths(qbs.installRoot, project.qmlDirectory)

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  QML                                                                                       //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Group {
        name: "QML"
        prefix: 'qml/'
        files: ['**/*.qml', '**/qmldir']
    }
    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Install                                                                                   //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Group {
        condition: project.qmlDirectory !== undefined
        fileTagsFilter: ['dynamiclibrary']
        qbs.install: true
        qbs.installDir: FileInfo.joinPaths(project.qmlDirectory, uri.replace(/\./g, '/'))
    }
}
