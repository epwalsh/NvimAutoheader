# =============================================================================
# File Name:     NvimAutoheader.py
# Author:        Evan 'Pete' Walsh
# Contact:       epwalsh@iastate.edu
# Creation Date: 2016-06-16
# Last Modified: 2017-06-22 13:24:03
# LICENSE:       The MIT License
#
#    Copyright (c) 2016 Evan Pete Walsh
#
#    Permission is hereby granted, free of charge, to any person obtaining a 
#    copy of this software and associated documentation files (the "Software"), 
#    to deal in the Software without restriction, including without limitation 
#    the rights to use, copy, modify, merge, publish, distribute, sublicense, 
#    and/or sell copies of the Software, and to permit persons to whom the 
#    Software is furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in 
#    all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
#    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
#    DEALINGS IN THE SOFTWARE.
#    
# =============================================================================

"""
Nvim Autoheader main functions.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
import os
from time import strftime

import neovim


filetypes = {
    'py': 'python', 
    'pyx': 'python',
    'r': 'R',
    'c': 'C', 
    'cpp': 'C', 
    'h': 'C', 
    'hpp': 'C',
    'sh': 'shell',
    'vim': 'vim',
    'js': 'javascript',
    'java': 'java',
    'jl': 'julia',
    'go': 'go',
    'rb': 'ruby',
    'php': 'PHP',
    'tex': 'tex',
}


styles = {
    'python': {
        'line_start': '#',  
        'prefix': None, 
        'postfix': None,
        'shebang': '#!/usr/bin/env python'
    },
    'vim': {
        'line_start': '"',  
        'prefix': None, 
        'postfix': None,
        'shebang': None
    },
    'R': {
        'line_start': '#',  
        'prefix': None, 
        'postfix': None,
        'shebang': None
    },
    'C': {
        'line_start': ' *', 
        'prefix': '/*', 
        'postfix': ' */',
        'shebang': None
    },
    'shell': {
        'line_start': '#',  
        'prefix': None, 
        'postfix': None,
        'shebang': '#!/usr/bin/env bash'
    },
    'javascript': {
        'line_start': ' *', 
        'prefix': '/*', 
        'postfix': ' */',
        'shebang': None
    },
    'java': {
        'line_start': ' *', 
        'prefix': '/*', 
        'postfix': ' */',
        'shebang': None
    },
    'julia': {
        'line_start': '#', 
        'prefix': None, 
        'postfix': None,
        'shebang': '#!/usr/bin/env julia'
    },
    'go': {
        'line_start': ' *', 
        'prefix': '/*', 
        'postfix': ' */',
        'shebang': None
    },
    'ruby': {
        'line_start': '#',  
        'prefix': None, 
        'postfix': None,
        'shebang': '#!/usr/local/bin/ruby -w'
    },
    'PHP': {
        'line_start': '//',  
        'prefix': None, 
        'postfix': None,
        'shebang': '#!/usr/bin/env php'
    },
    'tex': {
        'line_start': '%',
        'prefix': None,
        'postfix': None,
        'shebang': None,
    }
}


@neovim.plugin
class NvimAutoheader(object):

    def __init__(self, nvim):
        self.nvim = nvim

    def edit_name(self, filename):
        cb = self.nvim.current.buffer
        n = min([12, len(cb)])
        for index in range(n):
            if re.search(r'File Name:\s.*', cb[index]):
                cb[index] = re.sub(r'(^.*File Name:\s*)([^\s].*)$', r'\g<1>' + filename, cb[index])
    
    def edit_timestamp(self):
        cb = self.nvim.current.buffer
        time = strftime('%Y-%m-%d %H:%M:%S')
        n = min([12, len(cb)])
        for index in range(n):
            if re.search(r'Last Modified:.*', cb[index]):
                cb[index] = re.sub(r'(^.*Last Modified:).*$', r'\g<1> ' + time, cb[index])
    
    def find_header_end(self):
        cb = self.nvim.current.buffer
        n = min([12, len(cb)])
        for index in range(n):
            if re.search(r'Last Modified:.*', cb[index]):
                return index + 1
        return 0

    def format_wrap(self, width, start, stop):
        tw = self.nvim.eval('&tw')
        self.nvim.command('set formatoptions+=w')
        self.nvim.command('set tw=' + str(width - 1))
        self.nvim.command('normal! ' + str(start) + 'gggq' + str(stop) + 'gg')
        self.nvim.command('set tw=' + str(tw))

    def insert(self, paths, index, prefix=''):
        """
        Insert files from list of paths starting at 'index'.
        """
        for path in paths:
            cb = self.nvim.current.buffer
            n = self.nvim.eval('line("$")')
            self.nvim.command(str(index) + 'r ' + path)
            n = self.nvim.eval('line("$")') - n
            k = 0
            while k < n:
                cb[index + k] = prefix + cb[index + k]
                k += 1
            index += k
            self.insert_text(index, prefix)
            index += 1

    def insert_text(self, index, text):
        """
        Insert text into given line in buffer.
        """
        cb = self.nvim.current.buffer
        temp = cb[index:]
        cb[index] = text
        cb[(index + 1):] = temp

    def get_append_file(self, ext, path):
        if path[-1] != '/':
            path = path + '/'
        files = os.listdir(path)
        for fname in files:
            if re.search(r'.*\.' + ext + '$', fname):
                return path + fname
        return None
    
    def print_error(self, msg):
        self.nvim.command('echohl Error | echomsg "[NvimAutoheader] ' + msg + '" | echohl None')

    @neovim.function('Update_header', eval='expand("%:t")', sync=True)
    def on_file_write(self, args, filename):
        """
        Update the 'Last Modified' time when file is written.
        This also updates the name of the file in the header in case that has 
        changed.
        """
        cb = self.nvim.current.buffer
        self.edit_name(filename)
        self.edit_timestamp()
        self.nvim.command('set nomodified')

    @neovim.function('InsertHeader', eval='expand("%:t")')
    def insert_header(self, args, filename):
        """
        Insert the header at the top of file when new file is opened for the 
        first time.
        """
        ext = self.nvim.eval('expand("%:e")').lower()
        if ext not in filetypes.keys():
            return None

        ft              = filetypes[ext]
        line_start      = styles[ft]['line_start']
        cb              = self.nvim.current.buffer
        author          = self.nvim.eval('g:NvimAutoheader_author')
        org             = self.nvim.eval('g:NvimAutoheader_organization')
        contact         = self.nvim.eval('g:NvimAutoheader_contact')
        website         = self.nvim.eval('g:NvimAutoheader_website')
        width           = self.nvim.eval('g:NvimAutoheader_width')
        license         = self.nvim.eval('g:NvimAutoheader_license')
        license_verbose = self.nvim.eval('g:NvimAutoheader_license_verbose')
        append_path     = self.nvim.eval('g:NvimAutoheader_append_path')

        if styles[ft]['shebang'] is None:
            cb[0] = line_start + ' ' + ''.join('=' * (width - 3))
            if styles[ft]['prefix'] is not None:
                cb[0] = styles[ft]['prefix']
        else:
            cb[0] = styles[ft]['shebang']
            cb.append(line_start + ' ' + ''.join('=' * (width - 3)))

        cb.append(line_start + ' File Name:     ' + filename)

        if len(author) > 0:
            cb.append(line_start + ' Orig Author:   ' + author)
        if len(org) > 0:
            cb.append(line_start + ' Organization:  ' + org)
        if len(contact) > 0:
            cb.append(line_start + ' Contact:       ' + contact)
        if len(website) > 0:
            cb.append(line_start + ' Website:       ' + website)

        cb.append(line_start + ' Creation Date: ' + strftime('%Y-%m-%d'))
        cb.append(line_start + ' Last Modified: ')

        start = len(cb) + 1
        if len(license) > 0:
            if license_verbose > 0:
                path = self.nvim.eval('g:NvimAutoheader_location')
                if os.path.isfile(path + '/licenses/' + license):
                    cb.append(line_start + ' LICENSE:       ' + 'The ' + license + ' License')
                    with open(path + '/licenses/' + license, 'r') as f:
                        lines = f.read().splitlines()

                    cb.append(line_start)
                    cb.append(line_start + '    Copyright (c) ' + strftime('%Y') + ' ' + author)
                    cb.append(line_start)

                    for line in lines:
                        cb.append(line_start + '    ' + line)

                    cb.append(line_start)
                    self.format_wrap(width, start, len(cb))
                else:
                    self.print_error('no copy of this license found')
                    cb.append(line_start + ' LICENSE:       ' + license)
            else:
                cb.append(line_start + ' LICENSE:       ' + license)

        if styles[ft]['postfix'] is not None:
            cb.append(line_start + ' ' + ''.join('=' * (width - 4)))
            cb.append(styles[ft]['postfix'])
        else:
            cb.append(line_start + ' ' + ''.join('=' * (width - 3)))

        cb.append('')

        if append_path:
            append_file = self.get_append_file(ext, append_path)
            if append_file:
                self.nvim.current.window.cursor = [len(cb), 0]
                self.nvim.command('r %s' % append_file)

        #  cb.append('')

        self.nvim.current.window.cursor = [len(cb), 0]
        self.nvim.command('set nomodified')  

    @neovim.command('HeaderLicense', nargs=1)
    def insert_license(self, args):
        ext = self.nvim.eval('expand("%:e")').lower()
        if ext not in filetypes.keys():
            self.print_error("Sorry, we don't know how to handle this filetype yet")
            return None
        path = self.nvim.eval('g:NvimAutoheader_location')
        if not os.path.isfile(path + '/licenses/' + args[0]):
            self.print_error('no copy of this license found')
            return None

        cb = self.nvim.current.buffer
        n = len(cb)

        ft         = filetypes[ext]
        line_start = styles[ft]['line_start']
        author     = self.nvim.eval('g:NvimAutoheader_author')
        index      = self.find_header_end()
        width      = self.nvim.eval('g:NvimAutoheader_width')

        self.insert_text(index, line_start + ' LICENSE:       ' + 'The ' + args[0] + ' License')
        self.insert_text(index + 1, line_start)
        self.insert_text(index + 2, line_start + '    Copyright (c) ' + strftime('%Y') + ' ' + author)
        self.insert_text(index + 3, line_start)
        self.insert([path + '/licenses/' + args[0]], index + 4, line_start + '    ')
        self.format_wrap(width, index + 5, index + len(cb) - n)

    @neovim.command('HeaderAppend', nargs='*')
    def append_header(self, args):
        ext = self.nvim.eval('expand("%:e")').lower()
        if ext not in filetypes.keys():
            self.print_error("Sorry, we don't know how to handle this filetype yet")
            return None

        cb = self.nvim.current.buffer
        n = len(cb)

        ft         = filetypes[ext]
        line_start = styles[ft]['line_start']
        index      = self.find_header_end()
        width      = self.nvim.eval('g:NvimAutoheader_width')

        self.insert_text(index, line_start)
        self.insert(args, index + 1, line_start + ' ')
        self.format_wrap(width, index + 2, index + len(cb) - n)
