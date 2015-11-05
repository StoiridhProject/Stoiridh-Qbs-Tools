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

Product {
    id: root
    type: ['qdoc-html', 'qhp', 'qch']

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Dependencies                                                                              //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Depends { name: 'Qt.core' }

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Properties                                                                                //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    property path installDirectory: project.docDirectory
    property path installDocsDirectory: FileInfo.joinPaths(project.sourceDirectory, 'doc')
    property path projectDirectory: FileInfo.joinPaths(sourceDirectory, '..')
    property path docSourceDirectory: FileInfo.joinPaths(sourceDirectory, 'src')
    property string projectVersion: "1.0.0"
    property string baseName

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Configuration                                                                             //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Qt.core.qdocQhpFileName: baseName + '.qhp'
    Qt.core.qdocEnvironment: {
        var env = [];
        env.push('STOIRIDH_INSTALL_DOCS=' + root.installDocsDirectory);
        env.push('PROJECT_DIR=' + root.projectDirectory);
        env.push('SOURCE_DIR=' + root.docSourceDirectory);

        var projectVersion = root.projectVersion;
        env.push('PROJECT_VERSION=' + projectVersion);
        env.push('PROJECT_VERSION_TAG=' + projectVersion.replace(/\./g, ''));

        var docPath = Qt.core.docPath;
        env.push('QDOC_INDEX_DIR=' + docPath);
        env.push('QT_INSTALL_DOCS=' + docPath);

        return env;
    }
    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Sources                                                                                   //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    files: ['src/*.qdoc']

    Group {
        name: "QDoc Configuration"
        fileTags: 'qdocconf-main'
        files: '*.qdocconf'
    }
    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Install                                                                                   //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Group {
        condition: project.docDirectory !== undefined
        fileTagsFilter: 'qch'
        qbs.install: true
        qbs.installDir: project.docDirectory
    }

    Group {
        condition: project.docDirectory !== undefined
        fileTagsFilter: 'qdoc-html'
        qbs.install: true
        qbs.installDir: FileInfo.joinPaths(project.docDirectory, baseName)
    }
}
