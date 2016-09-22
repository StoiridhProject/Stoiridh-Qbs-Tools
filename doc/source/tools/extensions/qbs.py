# -*- coding: utf-8 -*-
"""
    stoiridh.sphinx.domains.qbs
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The Qbs domain.

    :copyright: Copyright 2016 Stòiridh Project.
    :license: BSD, see LICENCE.BSD for details.
"""
import re

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, Index, ObjType
from sphinx.locale import _, l_
from sphinx.roles import XRefRole
from sphinx.util.nodes import make_refnode

# RE for both a Qbs module and a Qbs item.
qbs_sig_re = re.compile(r'^(?P<name>[\w]+)$')

# RE for a Qbs property
qbs_prop_sig_re = re.compile(r'''
^(\w+\s)                                # property type
 (\w+\s?)                               # identifier name
 (?:\:\s                                # default value:
 (?:([\w\.]+\((?:[\w\s\.\,\'\"\-]+)?\)  #   a function
  |\d+[\.\,\d]*                         #   a numerical value
  |[\"\'][\w\.]*[\"\']                  #   a string
  |\w+)))?                              #   a variable or a keyword
$
''', re.VERBOSE)


class QbsSDK(Directive):
    """Directive to mark description of a new SDK. A SDK is a collection of items and modules."""
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False

    option_spec = {
        'synopsis': lambda x: x,
        'noindex': directives.flag
    }

    def run(self):
        sdkname = self.arguments[0].strip()
        env = self.state.document.settings.env
        env.ref_context['qbs:sdk'] = sdkname

        if 'noindex' in self.options:
            return []

        env.domaindata['qbs']['sdks'][sdkname] = (env.docname, self.options.get('synopsis', ''))
        env.domaindata['qbs']['objects'][sdkname] = (env.docname, 'sdk')

        # target
        targetname = 'sdk-' + sdkname
        targetnode = nodes.target('', '', ids=[targetname], ismod=True)
        self.state.document.note_explicit_target(targetnode)

        # index
        itext = _('%s (Qbs SDK)') % sdkname
        inode = addnodes.index(entries=[('single', itext, targetname, '', None)])

        return [targetnode, inode]


class QbsCurrentSDK(Directive):
    """This directive is just to tell Sphinx that we're documenting stuff in SDK foo, but links
    to SDK foo won't lead here."""
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False

    def run(self):
        sdkname = self.arguments[0].strip()
        env = self.state.document.settings.env

        if sdkname == 'None':
            env.ref_context.pop('qbs:sdk', None)
        else:
            env.ref_context['qbs:sdk'] = sdkname

        return []


class QbsPackage(Directive):
    """Directive to mark description of a new Package."""
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False

    option_spec = {
        'synopsis': lambda x: x,
        'noindex': directives.flag,
        'sdk': directives.unchanged
    }

    def run(self):
        pkgname = self.arguments[0].strip()
        env = self.state.document.settings.env
        env.ref_context['qbs:package'] = pkgname

        if 'noindex' in self.options:
            return []

        sdkname = self.options.get('sdk', env.ref_context.get('qbs:sdk', None))

        if sdkname:
            pkgname = sdkname + '.' + pkgname

        env.domaindata['qbs']['packages'][pkgname] = (env.docname, self.options.get('synopsis', ''))
        env.domaindata['qbs']['objects'][pkgname] = (env.docname, 'package')

        # target
        targetname = 'package-' + pkgname
        targetnode = nodes.target('', '', ids=[targetname], ismod=True)
        self.state.document.note_explicit_target(targetnode)

        # index
        if sdkname:
            itext = _('%s (Qbs Package in %s)') % (pkgname[len(sdkname) + 1:], sdkname)
        else:
            itext = _('%s (Qbs Package') % (pkgname[len(sdkname) + 1:])
        inode = addnodes.index(entries=[('single', itext, targetname, '', None)])

        return [targetnode, inode]


class QbsCurrentPackage(Directive):
    """This directive is just to tell Sphinx that we're documenting stuff in Package foo, but
    links to Package foo won't lead here."""
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False

    def run(self):
        pkgname = self.arguments[0].strip()
        env = self.state.document.settings.env

        if pkgname == 'None':
            env.ref_context.pop('qbs:package', None)
        else:
            env.ref_context['qbs:package'] = pkgname

        return []


class QbsObject(ObjectDescription):
    """Base object description for all Qbs objects."""
    has_content = True
    option_spec = {
        'noindex': directives.flag,
        'sdk': directives.unchanged,
    }

    def get_signature_prefix(self):
        """Return the signature prefix. By default, it returns the object type, :py:attr:`objtype`
        following by a space.
        """
        return self.objtype + ' '

    def parse(self, sig):
        """Parse the signature and return a tuple with 3 items:

        * `type` --- the type of the object
        * `name` --- the name of the object
        * `value` --- the default value of the value

        Any of those items may return a :py:obj:`None` type except for the *name* item that should
        return a valid value.
        """
        raise NotImplementedError("must be implemented in subclasses")

    def get_signature_name(self, **kwargs):
        """Return the signature name that identify the object in a cross-reference search."""
        raise NotImplementedError("must be implemented in subclasses")

    def update_domaindata(self, fullname, objtype):
        """Update the domain data."""
        pass

    def handle_signature(self, sig, signode):
        sdkname = self.options.get('sdk', self.env.ref_context.get('qbs:sdk'))
        pkgname = self.options.get('package', self.env.ref_context.get('qbs:package'))
        modname = self.env.ref_context.get('qbs:module', None)
        itemname = self.env.ref_context.get('qbs:item', None)

        type, name, value = self.parse(sig)

        signode['module'] = modname
        signode['package'] = pkgname
        signode['item'] = itemname

        if self.objtype == 'property':
            fullname = self.get_signature_name(objname=(modname or itemname), name=name)
        else:
            fullname = name

        signode['sdk'] = sdkname
        signode['fullname'] = fullname

        sigprefix = self.get_signature_prefix()
        if sigprefix:
            signode += addnodes.desc_annotation(sigprefix, sigprefix)
        if type:
            signode += addnodes.desc_addname(type, type)
        if name:
            signode += addnodes.desc_name(name, name)
        if value:
            signode += addnodes.desc_returns(value, value)

        return fullname

    def get_index_text(self, sdkname, name):
        """Return the text for the index entry of the object."""
        if sdkname:
            itext = '%s (Qbs %s in %s)' % (name, self.objtype.capitalize(), sdkname)
        else:
            itext = '%s (Qbs %s)' % (name, self.objtype.capitalize())
        return itext

    def add_target_and_index(self, name, sig, signode):
        sdkname = self.options.get('sdk', self.env.ref_context.get('qbs:sdk'))
        pkgname = self.options.get('package', self.env.ref_context.get('qbs:package'))

        name_prefix = (sdkname and sdkname + '.' or '') + (pkgname and pkgname + '.' or '')
        fullname = name_prefix + name

        if fullname not in self.state.document.ids:
            signode['names'].append(fullname)
            signode['ids'].append(fullname)
            signode['first'] = (not self.names)
            self.state.document.note_explicit_target(signode)

            objects = self.env.domaindata['qbs']['objects']

            if fullname in objects:
                message = '''duplicate object description of %s, other instance in %s, use :noindex:
                             for one of them''' % (fullname,
                                                   self.env.doc2path(objects[fullname][0]))
                self.state_machine.reporter.warning(message, lineno=self.lineno)

            objects[fullname] = (self.env.docname, self.objtype)

            self.update_domaindata(fullname, self.objtype)

        itext = self.get_index_text(sdkname, name)
        if itext:
            self.indexnode['entries'].append(('single', itext, fullname, '', None))


class QbsItemObject(QbsObject):
    """Object description for a Qbs item."""
    option_spec = {
        'noindex': directives.unchanged,
        'sdk': directives.unchanged,
        'package': directives.unchanged,
        'synopsis': lambda x: x
    }

    def get_signature_name(self, objname, name, **kwargs):
        return name

    def parse(self, sig):
        """Parse the signature for a Qbs Item and return a tuple with 3 items:
        (None, name, None)."""
        m = qbs_sig_re.match(sig)

        if not m:
            self.state_machine.reporter.error(_('%s is not a valid Qbs %s signature.') %
                                              (sig, self.objtype), line=self.lineno)
            raise ValueError

        return (None, m.group('name'), None)

    def update_domaindata(self, fullname, objtype):
        if self.objtype == objtype:
            self.env.domaindata['qbs']['items'][fullname] = (self.env.docname,
                                                             self.options.get('synopsis', ''))

    def get_index_text(self, sdkname, name):
        """Return the text for the index entry of an item."""
        pkgname = self.options.get('package', self.env.ref_context.get('qbs:package', None))
        if pkgname:
            pkgname = (sdkname and sdkname + '.' + pkgname or pkgname)
        return super().get_index_text(pkgname, name)

    def before_content(self):
        super().before_content()
        if self.names:
            self.env.ref_context['qbs:item'] = self.names[0]
            # update the *qbs:package* from the reference context if the user has set the *package*
            # option.
            pkgname = self.options.get('package', self.env.ref_context.get('qbs:package', None))
            if pkgname:
                self.env.ref_context['qbs:package'] = pkgname
            # we'll now document the properties for a Qbs item, so we do remove 'qbs:module' from
            # the reference context.
            self.env.ref_context.pop('qbs:module', None)


class QbsModuleObject(QbsObject):
    """Object description for a Qbs module."""
    option_spec = {
        'noindex': directives.unchanged,
        'sdk': directives.unchanged,
        'synopsis': lambda x: x
    }

    def get_signature_name(self, objname, name, **kwargs):
        return name

    def parse(self, sig):
        """Parse the signature for a Qbs module and return a tuple with 3 items:
        (None, name, None)."""
        m = qbs_sig_re.match(sig)
        if not m:
            self.state_machine.reporter.error(_('%s is not a valid Qbs %s signature.') %
                                              (sig, self.objtype), line=self.lineno)
            raise ValueError
        return (None, m.group('name'), None)

    def update_domaindata(self, fullname, objtype):
        if self.objtype == objtype:
            self.env.domaindata['qbs']['modules'][fullname] = (self.env.docname,
                                                               self.options.get('synopsis', ''))

    def before_content(self):
        super().before_content()
        if self.names:
            self.env.ref_context['qbs:module'] = self.names[0]
            # we'll now document the properties for a Qbs module, so we do remove both 'qbs:item'
            # and 'qbs:package' from the reference context.
            self.env.ref_context.pop('qbs:item', None)
            self.env.ref_context.pop('qbs:package', None)


class QbsPropertyObject(QbsObject):
    """Object description that represents a property for a Qbs module or a Qbs item."""
    option_spec = {
        'readonly': directives.flag
    }

    def get_signature_name(self, objname, name, **kwargs):
        return objname + '.' + name

    def parse(self, sig):
        """Parse the signature for a Qbs property and return a tuple with 3 items:
        (type, name[, value])."""
        m = qbs_prop_sig_re.match(sig)
        if not m:
            self.state_machine.reporter.error(_('%s is not a valid Qbs %s signature.') %
                                              (sig, self.objtype), line=self.lineno)
            raise ValueError
        return m.groups()

    def get_signature_prefix(self):
        """Return the signature prefix of the property. If the *readonly* option is specified, then
        *readonly* will be added at first."""
        return ('readonly ' if 'readonly' in self.options else '') + self.objtype + ' '

    def get_index_text(self, sdkname, name):
        """Return the text for the index entry of a property."""
        pkgname = self.env.ref_context.get('qbs:package', None)

        dot = name.rfind('.')

        if dot != -1:
            property_name = name[dot + 1:]
            owner = name[:dot]
        else:
            property_name = name
            owner = ''

        if sdkname and owner:
            prefix = (pkgname and '.'.join((sdkname, pkgname, owner)) or
                      '.'.join((sdkname, owner)))
            itext = '%s (%s Qbs %s)' % (property_name, prefix, self.objtype.capitalize())
        else:
            prefix = (pkgname and '.'.join((pkgname, property_name)) or property_name)
            itext = '%s (Qbs %s)' % (prefix, self.objtype.capitalize())

        return itext


# ref: https://github.com/sphinx-doc/sphinx/blob/1.4.1/sphinx/domains/python.py#L492

class QbsXRefRole(XRefRole):
    def process_link(self, env, refnode, has_explicit_title, title, target):
        refnode['qbs:sdk'] = env.ref_context.get('qbs:sdk')
        refnode['qbs:package'] = env.ref_context.get('qbs:package')
        refnode['qbs:module'] = env.ref_context.get('qbs:module')
        refnode['qbs:item'] = env.ref_context.get('qbs:item')

        if not has_explicit_title:
            title = title.lstrip('.')       # only has a meaning for the target
            target = target.lstrip('~')     # only has a meaning for the title
            # if the first character is a tilde, don't display the sdk/module/item
            # parts of the contents
            if title[0:1] == '~':
                title = title[1:]
                # special case: for the package directive we do remove the left part which
                # corresponds to the SDK's name.
                if refnode['reftype'] == 'pkg':
                    dot = title.find('.')
                else:
                    dot = title.rfind('.')

                if dot != -1:
                    title = title[dot + 1:]
        # if the first character is a dot, search more specific namespaces first
        # else search builtins first
        if target[0:1] == '.':
            target = target[1:]
            refnode['refspecific'] = True
        return title, target


class QbsObjectIndex(Index):
    """Index for the Qbs objects."""
    def get_sdk_synopsis(self, sdkname):
        sdks = self.domain.data['sdks']
        sdk = sdks.get(sdkname, '')
        return sdk and sdk[1] or ''

    def generate(self, docnames=None):
        raise NotImplementedError('must be implemented in subclasses')


class QbsItemIndex(QbsObjectIndex):
    """Index for the Qbs items."""
    name = 'itemindex'
    localname = l_('Qbs Item Index')
    shortname = l_('Qbs items')

    def generate(self, docnames=None):
        content = dict()
        items = self.domain.data['items']

        current_sdkname = ''
        subtype = 0

        for itemname, (docname, synopsis) in items.items():
            if docnames and docname not in docnames:
                continue

            entries = content.setdefault(itemname[0].lower(), [])
            sdkname = itemname.split('.')[0]

            if sdkname != itemname:
                if not current_sdkname.startswith(sdkname):
                    sdksynopsis = self.get_sdk_synopsis(sdkname)
                    entries.append([sdkname, 1, '', '', '', '', sdksynopsis])
                    current_sdkname = sdkname
                    subtype = 2
            else:
                subtype = 0

            entries.append([itemname, subtype, docname, itemname, '', '', synopsis])

        content = sorted(content.items())

        return content, False


class QbsModuleIndex(QbsObjectIndex):
    """Index for the Qbs modules."""
    name = 'modindex'
    localname = l_('Qbs Module Index')
    shortname = l_('Qbs modules')

    def generate(self, docnames=None):
        content = dict()
        modules = self.domain.data['modules']

        current_sdkname = ''
        subtype = 0

        for modname, (docname, synopsis) in modules.items():
            if docnames and docname not in docnames:
                continue

            entries = content.setdefault(modname[0].lower(), [])
            sdkname = modname.split('.')[0]

            if sdkname != modname:
                if not current_sdkname.startswith(sdkname):
                    sdksynopsis = self.get_sdk_synopsis(sdkname)
                    entries.append([sdkname, 1, '', '', '', '', sdksynopsis])
                    current_sdkname = sdkname
                    subtype = 2
            else:
                subtype = 0

            entries.append([modname, subtype, docname, modname, '', '', synopsis])

        content = sorted(content.items())

        return content, False


class QbsDomain(Domain):
    """Qbs language domain."""
    name = 'qbs'
    label = 'Qbs'

    object_types = {
        'sdk': ObjType(l_('sdk'), 'sdk'),
        'package': ObjType(l_('package'), 'pkg'),
        'item': ObjType(l_('item'), 'item'),
        'module': ObjType(l_('module'), 'mod'),
        'property': ObjType(l_('property'), 'prop')
    }

    directives = {
        'sdk': QbsSDK,
        'currentsdk': QbsCurrentSDK,
        'package': QbsPackage,
        'currentpackage': QbsCurrentPackage,
        'item': QbsItemObject,
        'module': QbsModuleObject,
        'property': QbsPropertyObject
    }

    roles = {
        'sdk': QbsXRefRole(),
        'pkg': QbsXRefRole(),
        'item': QbsXRefRole(),
        'mod': QbsXRefRole(),
        'prop': QbsXRefRole()
    }

    initial_data = {
        'sdks': {},     # sdkname -> docname, synopsis
        'packages': {},  # pkgname -> docname, synopsis
        'modules': {},  # modname -> docname, synopsis
        'items': {},    # itemname -> docname, synopsis
        'objects': {}   # fullname -> docname, objtype
    }

    indices = [
        QbsItemIndex,
        QbsModuleIndex
    ]

    def clear_doc(self, docname):
        for data in self.initial_data.keys():
            self._clear_doc(data, docname)

    def _clear_doc(self, data, docname):
        for name, (dn, _) in self.data[data].items():
            if dn == docname:
                del self.data[data][name]

    def merge_domaindata(self, docnames, otherdata):
        for data in self.initial_data.keys():
            self._merge_domaindata(data, docnames, otherdata)

    def _merge_domaindata(self, data, docnames, otherdata):
        for n, d in self.otherdata[data].items():
            if d[0] in docnames:
                self.data[data][n] = d

    def get_objects(self):
        for sdkname, (docname, synopsis) in self.data['sdks'].items():
            yield (sdkname, sdkname, 'sdk', docname, '', 0)
        for pkgname, (docname, synopsis) in self.data['packages'].items():
            yield (pkgname, pkgname, 'package', docname, '', 0)
        for modname, (docname, synopsis) in self.data['modules'].items():
            yield (modname, modname, 'module', docname, '', 0)
        for itemname, (docname, synopsis) in self.data['items'].items():
            yield (itemname, itemname, 'item', docname, '', 0)
        for fullname, (docname, objtype) in self.data['objects'].items():
            if objtype not in ('sdk', 'package', 'module', 'item'):
                yield (fullname, fullname, objtype, docname, '', 1)

    def find_objects(self, env, sdkname, modname, pkgname, itemname, name, type, searchmode):
        if not name:
            return []

        objects = self.data['objects']
        matches = list()
        newname = None

        # we are in a reference specific search where we do complete the given name and then search
        # in the objects dictionary in order to find it.
        if searchmode:
            objtypes = self.objtypes_for_role(type)
            if objtypes:
                if sdkname:
                    if pkgname and not name.startswith(pkgname):
                        newname = '.'.join((sdkname, pkgname, name))
                    elif modname and not name.startswith(modname):
                        newname = '.'.join((sdkname, modname, name))
                    else:
                        newname = '.'.join((sdkname, name))
                    if newname in objects:
                        matches.append((newname, objects[newname]))
                    else:
                        newname = None
                # if we have not found the name, then try a "fuzzy" search.
                if not newname:
                    searchname = '.' + name
                    matches = [(objname, objects[objname]) for objname in objects
                               if objname.endswith(searchname) and objects[objname][1] in objtypes]
        else:
            # fully qualified name makes the search easier.
            if name in objects:
                matches.append((name, objects[name]))
            elif sdkname:
                if modname:
                    # searching a *name* for a module which is relative to the current document.
                    if name.startswith(modname):
                        newname = '.'.join((sdkname, name))
                    else:
                        newname = '.'.join((sdkname, modname, name))
                elif itemname:
                    # searching a *name* for an item which is relative to the current document.
                    if pkgname:
                        if name.startswith(itemname):
                            newname = '.'.join((sdkname, pkgname, name))
                        else:
                            newname = '.'.join((sdkname, pkgname, itemname, name))
                    else:
                        if name.startswith(itemname):
                            newname = '.'.join((sdkname, name))
                        else:
                            newname = '.'.join((sdkname, itemname, name))
                if newname in objects:
                    matches.append((newname, objects[newname]))

        return matches

    def resolve_xref(self, env, fromdocname, builder, type, target, node, contnode):
        sdkname = node.get('qbs:sdk')
        pkgname = node.get('qbs:package')
        modname = node.get('qbs:module')
        itemname = node.get('qbs:item')
        searchmode = node.hasattr('refspecific')

        matches = self.find_objects(env, sdkname, modname, pkgname, itemname, target, type,
                                    searchmode)

        if not matches:
            return None
        elif len(matches) > 1:
            env.warn_node('more than one target found for cross-reference %r: %s' %
                          (target, ', '.join(match[0] for match in matches)), node)

        name, obj = matches[0]

        if obj[1] == 'sdk':
            return self._make_sdk_refnode(builder, fromdocname, name, contnode)
        elif obj[1] == 'package':
            return self._make_package_refnode(builder, fromdocname, name, contnode)
        elif obj[1] == 'module':
            return self._make_module_refnode(builder, fromdocname, name, contnode)
        elif obj[1] == 'item':
            return self._make_item_refnode(builder, fromdocname, name, contnode)
        else:
            return make_refnode(builder, fromdocname, obj[0], name, contnode, name)

    def _make_sdk_refnode(self, builder, fromdocname, name, contnode):
        """Make a reference node for a Qbs SDK."""
        docname, synopsis = self.data['sdks'][name]
        title = name
        if synopsis:
            title += ': ' + synopsis
        return make_refnode(builder, fromdocname, docname, 'sdk-' + name, contnode, title)

    def _make_package_refnode(self, builder, fromdocname, name, contnode):
        """Make a reference node for a Qbs package."""
        docname, synopsis = self.data['packages'][name]
        title = name
        if synopsis:
            title += ': ' + synopsis
        return make_refnode(builder, fromdocname, docname, 'package-' + name, contnode, title)

    def _make_module_refnode(self, builder, fromdocname, name, contnode):
        """Make a reference node for a Qbs module."""
        docname, synopsis = self.data['modules'][name]
        title = name
        if synopsis:
            title += ': ' + synopsis
        return make_refnode(builder, fromdocname, docname, name, contnode, title)

    def _make_item_refnode(self, builder, fromdocname, name, contnode):
        """Make a reference node for a Qbs item."""
        docname, synopsis = self.data['items'][name]
        title = name
        if synopsis:
            title += ': ' + synopsis
        return make_refnode(builder, fromdocname, docname, name, contnode, title)


def setup(app):
    app.add_domain(QbsDomain)
    return {'version': '0.1.0-alpha', 'parallel_read_safe': True}
