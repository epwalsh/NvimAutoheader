# =============================================================================
# File Name:     NvimAutoheader.py
# Author:        Evan 'Pete' Walsh
# Contact:       epwalsh@iastate.edu
# Creation Date: 2016-06-16
# Last Modified: 2016-06-16 18:25:50
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


# Need to fix this insert function
def insert(cb, index, item):
    temp = cb[index]
    cb[index] = item
    if len(cb) <= (index + 1):
        cb.append(temp)
    else:
        cb[index + 1] = temp


@neovim.plugin
class NvimAutoheader(object):
    def __init__(self, nvim):
        self.nvim = nvim

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
            with open(path, 'r') as f:
                lines = f.read().splitlines()
            insert(cb, index, line_start)
            index += 1
            for line in lines:
                insert(cb, index, line_start + ' ' + line)
                index += 1
