# =============================================================================
# File Name:     NvimAutoheader.py
# Author:        Evan 'Pete' Walsh
# Contact:       epwalsh@iastate.edu
# Creation Date: 2016-06-16
# Last Modified: 2016-06-17 00:32:23
# =============================================================================

import neovim
import re
from time import strftime

filetypes = {
    'py': 'python',
    'r': 'R',
    'c': 'C', 'cpp': 'C', 'h': 'C', 'hpp': 'C',
    'sh': 'bash',
    'vim': 'vim',
    'js': 'javascript'
}


styles = {
    'python':     {'line_start': '#',  'prefix': None, 'postfix': None,
                   'shebang': '#!/usr/bin/env python'},
    'vim':        {'line_start': '"',  'prefix': None, 'postfix': None,
                   'shebang': None},
    'R':          {'line_start': '#',  'prefix': None, 'postfix': None,
                   'shebang': None},
    'C':          {'line_start': ' *', 'prefix': '/*', 'postfix': ' */',
                   'shebang': None},
    'bash':       {'line_start': '#',  'prefix': None, 'postfix': None,
                   'shebang': '#!/bin/bash'},
    'javascript': {'line_start': ' *', 'prefix': '/*', 'postfix': ' */',
                   'shebang': None}
}


def edit_name(cb, filename):
    n = min([12, len(cb)])
    for index in range(n):
        if re.search(r'File Name:\s.*', cb[index]):
            cb[index] = re.sub(r'(^.*File Name:\s*)([^\s].*)$', r'\1' + filename, cb[index])


def edit_timestamp(cb):
    time = strftime('%Y-%m-%d %H:%M:%S')
    n = min([12, len(cb)])
    for index in range(n):
        if re.search(r'Last Modified:.*', cb[index]):
            cb[index] = re.sub(r'(^.*Last Modified:).*$', r'\1 ' + time, cb[index])


def find_header_end(cb):
    n = min([12, len(cb)])
    for index in range(n):
        if re.search(r'Last Modified:.*', cb[index]):
            return index + 1


@neovim.plugin
class NvimAutoheader(object):
    def __init__(self, nvim):
        self.nvim = nvim
        #  self._author = self.nvim.eval('g:NvimAutoheader_author')
        #  self._contact = self.nvim.eval('g:NvimAutoheader_contact')
        #  self._website = self.nvim.eval('g:NvimAutoheader_website')
        #  self._width = self.nvim.eval('g:NvimAutoheader_width')
        #  self._license = self.nvim.eval('g:NvimAutoheader_license')
        #  self._license_verbose = self.nvim.eval('g:NvimAutoheader_license_verbose')

    #  @neovim.autocmd('FileWritePre', pattern='*.*', eval='expand("<afile>")', sync=True)
    @neovim.function('Update_header', eval='expand("<afile>")', sync=True)
    def on_file_write(self, args, filename):
        """
        Update the 'Last Modified' time when file is written.
        This also updates the name of the file in the header in case that has 
        changed.
        """
        cb = self.nvim.current.buffer
        edit_name(cb, filename)
        edit_timestamp(cb)
        self.nvim.command('set nomodified')

    #  @neovim.autocmd('BufWritePre', pattern='*.*', eval='expand("<afile>")', sync=True)
    #  def on_buf_write(self, filename):
        #  cb = self.nvim.current.buffer
        #  edit_name(cb, filename)
        #  edit_timestamp(cb)
        #  self.nvim.command('set nomodified')

    def format_wrap(self, width, start):
        tw = self.nvim.eval('&tw')
        self.nvim.command('set formatoptions+=w')
        self.nvim.command('set tw=' + str(width - 1))
        self.nvim.command('normal! ' + str(start) + 'gggqG')
        self.nvim.command('set tw=' + str(tw))

    #  @neovim.autocmd('BufNewFile', pattern='*.*', eval='expand("<afile>")')
    @neovim.function('InsertHeader', eval='expand("<afile>")')
    def insert_header(self, args, filename):
        """
        Insert the header at the top of file when new file is opened for the 
        first time.
        """
        ext = self.nvim.eval('expand("%:e")').lower()
        if ext not in filetypes.keys():
            return None

        ft = filetypes[ext]
        line_start = styles[ft]['line_start']
        cb = self.nvim.current.buffer
        author = self.nvim.eval('g:NvimAutoheader_author')
        contact = self.nvim.eval('g:NvimAutoheader_contact')
        website = self.nvim.eval('g:NvimAutoheader_website')
        width = self.nvim.eval('g:NvimAutoheader_width')
        license = self.nvim.eval('g:NvimAutoheader_license')
        license_verbose = self.nvim.eval('g:NvimAutoheader_license_verbose')

        if styles[ft]['shebang'] is None:
            cb[0] = line_start + ' ' + ''.join('=' * (width - 3))
            if styles[ft]['prefix'] is not None:
                cb[0] = styles[ft]['prefix']
        else:
            cb[0] = styles[ft]['shebang']
            cb.append(line_start + ' ' + ''.join('=' * (width - 3)))
        cb.append(line_start + ' File Name:     ' + filename)
        if len(author) > 0:
            cb.append(line_start + ' Author:        ' + author)
        if len(contact) > 0:
            cb.append(line_start + ' Contact:       ' + contact)
        if len(website) > 0:
            cb.append(line_start + ' Website:       ' + website)
        cb.append(line_start + ' Creation Date: ' + strftime('%Y-%m-%d'))
        cb.append(line_start + ' Last Modified: ')
        start = len(cb) + 1
        if len(license) > 0:
            if license_verbose > 0:
                cb.append(line_start + ' LICENSE:       ' + 'The ' + license + ' License')
                path = self.nvim.eval('g:NvimAutoheader_location')
                with open(path + '/licenses/' + license, 'r') as f:
                    lines = f.read().splitlines()
                cb.append(line_start)
                cb.append(line_start + '    Copyright (c) ' + strftime('%Y') + ' ' + author)
                cb.append(line_start)
                for line in lines:
                    cb.append(line_start + '    ' + line)
                cb.append(line_start)
                self.format_wrap(width, start)
            else:
                cb.append(line_start + ' LICENSE:       ' + license)
        if styles[ft]['postfix'] is not None:
            cb.append(line_start + ' ' + ''.join('=' * (width - 4)))
            cb.append(styles[ft]['postfix'])
        else:
            cb.append(line_start + ' ' + ''.join('=' * (width - 3)))
        cb.append('')
        cb.append('')

        self.nvim.current.window.cursor = [len(cb), 0]
        self.nvim.command('set nomodified')

    @neovim.command('NvimAutoheaderAppend', range='', nargs='*')
    def append_header(self, args, range):
        #  self.nvim.current.line = ('Command with args: {}, range: {}' .format(args, range))
        ext = self.nvim.eval('expand("%:e")').lower()
        if ext not in filetypes.keys():
            self.nvim.command('echom "[NvimAutoheader] Unknown filetype"')
            return None

        ft = filetypes[ext]
        line_start = styles[ft]['line_start']
        cb = self.nvim.current.buffer
        index = find_header_end(cb)

        for path in args:
            n = self.nvim.eval('line("$")')
            self.nvim.command(str(index) + 'r ' + path)
            n = self.nvim.eval('line("$")') - n
            self.nvim.command('echom ' + str(n))
            k = 0
            while k < n:
                cb[index + k] = line_start + ' ' + cb[index + k]
                k += 1

        #  for path in args:
            #  with open(path, 'r') as f:
                #  lines = f.read().splitlines()
            #  insert(cb, index, line_start)
            #  index += 1
            #  for line in lines:
                #  insert(cb, index, line_start + ' ' + line)
                #  index += 1
