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
import qbs.Process
import Stoiridh.Utils

Probe {
    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Input properties                                                                          //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    property string minimumVersion

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Output properties                                                                         //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    property path path
    property path filePath
    property string version

    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Configure                                                                                 //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    configure: {
        var environmentPaths = qbs.getEnv('PATH').split(qbs.pathListSeparator);
        var filePaths = [];

        if (qbs.hostOS.contains('linux')) {
            var fileNames = ['python', 'python2', 'python3'];

            for (var i in fileNames) {
                var fp = FileInfo.joinPaths('/usr/bin', fileNames[i]);

                if (File.exists(fp))
                    filePaths.push(fp);
            }
        } else if (qbs.hostOS.contains('windows')) {
            var fileNames = ['python.exe', 'py.exe'];

            for (var i in fileNames) {
                for (var j in environmentPaths) {
                    var fp = FileInfo.joinPaths(environmentPaths[j], fileNames[i]);

                    if (File.exists(fp) && FileInfo.isAbsolutePath(fp))
                        filePaths.push(fp);
                }
            }

            // Python not found in the environment paths, try Windows directory instead.
            if (filePaths.length === 0) {
                var fp = FileInfo.joinPaths(qbs.getEnv('WINDIR'), 'py.exe');

                if (File.exists(fp) && FileInfo.isAbsolutePath(fp))
                    filePaths.push(fp);
            }
        }

        // checks the versions of python
        for (var i in filePaths) {
            var process;
            var output = '';
            try {
                process = new Process();
                process.exec(filePaths[i], ['--version'], true);
                output = process.readStdOut().split('\n')[0];
            } catch (e) {
                print(e.fileName + ':' + e.lineNumber + ':', e.message);
            } finally {
                if (process)
                    process.close();
            }

            var v = Utils.checkVersion(output, minimumVersion);

            if (v.isValid) {
                filePath = filePaths[i];
                path = FileInfo.path(filePath);
                version = v.version;
                found = true;
                break;
            }
        }
    }
}
