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
import Stoiridh.Internal

Module {
    name: 'QtDocumentation'
    additionalProductTypes: ['stoiridh.internal.python.qdoc-html', 'qhp', 'qch']

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Dependencies                                                                              //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Depends { id: python; name: 'Python'; required: true }
    Depends { name: 'Qt.core' }

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Configuration                                                                             //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Qt.core.qdocQhpFileName: baseName + '.qhp'
    Qt.core.qdocEnvironment: {
        var env = [];
        env.push('STOIRIDH_INSTALL_DOCS=' + installDocsDirectory);
        env.push('PROJECT_DIR=' + projectDirectory);
        env.push('SOURCE_DIR=' + sourceDirectory);

        env.push('PROJECT_VERSION=' + projectVersion);
        env.push('PROJECT_VERSION_TAG=' + projectVersion.replace(/\./g, ''));

        var docPath = Qt.core.docPath;
        env.push('QDOC_INDEX_DIR=' + docPath);
        env.push('QT_INSTALL_DOCS=' + docPath);

        return env;
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Properties                                                                                //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    property string baseName
    property string installDocsDirectory
    property string projectDirectory
    property string sourceDirectory
    property string projectVersion

    property string installDirectory

    /*! \internal */
    property stringList qbsSearchPaths

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Validate                                                                                  //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    validate: {
        var validator = new ModUtils.PropertyValidator('Qt.Documentation');
        // properties required by qdoc
        validator.setRequiredProperty('baseName', baseName);
        validator.setRequiredProperty('installDocsDirectory', installDocsDirectory);
        validator.setRequiredProperty('projectDirectory', projectDirectory);
        validator.setRequiredProperty('sourceDirectory', sourceDirectory);
        validator.setRequiredProperty('projectVersion', projectVersion);

        // install property
        validator.setRequiredProperty('installDirectory', installDirectory);

        // internal property
        validator.setRequiredProperty('qbsSearchPaths', qbsSearchPaths);
        validator.validate();
    }
    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Rules                                                                                     //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Rule {
        condition: python.condition && python.found
        inputs: ['qdoc-html']
        explicitlyDependsOn: ['qch']

        Artifact {
            fileTags: ['stoiridh.internal.python.qdoc-html']
            filePath: '.deps'
            alwaysUpdated: false
        }

        prepare: {
            var generatedFilesDir = FileInfo.joinPaths(product.buildDirectory, 'GeneratedFiles');
            var qbsSearchPaths = ModUtils.moduleProperties(product, 'qbsSearchPaths');
            var script = Internal.getPythonScript('python/stoiridh.py', qbsSearchPaths);
            var python = product.moduleProperty('Python', 'filePath');

            var installDirectory = ModUtils.moduleProperty(product, 'installDirectory');
            var baseName = ModUtils.moduleProperty(product, 'baseName');

            // arguments
            var args = [script, 'doc', baseName, generatedFilesDir, installDirectory];

            var cmd = new Command(python, args);
            cmd.description = 'copying documentation for ' + product.name;
            cmd.highlight = 'filegen';
            return cmd;
        }
    }
}
