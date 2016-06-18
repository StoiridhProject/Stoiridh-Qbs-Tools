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
var Version = loadExtension('Stoiridh.Utils.Version');

function checkVersion(input, minimum) {
    try {
        var inputVersion = Version.VersionNumber.fromString(input);
        var minimumVersion = Version.VersionNumber.fromString(minimum);
    } catch (e) {
        print(e.fileName + ':' + e.lineNumber + ':', e.message);
    }

    return {
        isValid: (inputVersion.compareTo(minimumVersion) >= 0),
        version: inputVersion.toString()
    };
}

/* Checks if the given \a inputs are valid properties. */
function isValidProperties(inputs) {
    if (Array.isArray(inputs)) {
        for (var i in inputs) {
            if (!isValidProperty(inputs[i])) {
                return false;
            }
        }
    } else {
        throw "isValidProperties: inputs parameter must be an array!";
    }

    return true;
}

/* Checks if the given \a input is a valid property. */
function isValidProperty(input) {
    if (input === undefined || input === null) {
        return false;
    } else if (typeof input === 'string' && input === '') {
        return false;
    }

    return true;
}

/* Returns \a input if it is a valid property, otherwise \a defaultValue. */
function getProperty(input, defaultValue) {
    return isValidProperty(input) ? input : defaultValue;
}
