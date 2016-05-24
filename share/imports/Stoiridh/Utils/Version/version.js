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
var VersionNumber = (function() {
    function VersionNumber(major, minor, patch) {
        if (major === undefined) { major = 1; }
        if (minor === undefined) { minor = 0; }
        if (patch === undefined) { patch = 0; }

        this.m_major = major;
        this.m_minor = minor;
        this.m_patch = patch;
    }
    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Properties                                                                                //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    Object.defineProperty(VersionNumber.prototype, 'major', {
        get: function() { return this.m_major; },
        set: function(value) { this.m_major = value; }
    });
    Object.defineProperty(VersionNumber.prototype, 'minor', {
        get: function() { return this.m_minor; },
        set: function(value) { this.m_minor = value; }
    });
    Object.defineProperty(VersionNumber.prototype, 'patch', {
        get: function() { return this.m_patch; },
        set: function(value) { this.m_patch = value; }
    });
    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Methods                                                                                   //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    VersionNumber.prototype.toString = function() {
        return this.m_major + '.' + this.m_minor + '.' + this.m_patch;
    };
    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Operators                                                                                 //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    VersionNumber.prototype.equals = function(rhs) {
        return (this.m_major === rhs.m_major
            && this.m_minor === rhs.m_minor
            && this.m_patch === rhs.m_patch);
    };
    VersionNumber.prototype.compareTo = function(rhs) {
        if (this.equals(rhs)) {
            return 0;
        } else if (this.m_major < rhs.m_major
            || (this.m_major === rhs.m_major && this.m_minor < rhs.m_minor)
            || (this.m_minor === rhs.m_minor && this.m_patch < rhs.m_patch)) {
            return -1;
        } else {
            return 1;
        }
    };
    ////////////////////////////////////////////////////////////////////////////////////////////////
    //  Static methods                                                                            //
    ////////////////////////////////////////////////////////////////////////////////////////////////
    VersionNumber.fromString = function(str) {
        var match = str.match(/(\d+(?:\.\d+){0,2})/);

        if (match <= 0)
            throw new RangeError('Invalid version string');

        var version = match[0].split('.');

        return new VersionNumber(version[0], version[1], version[2]);
    };

    return VersionNumber;
})();
