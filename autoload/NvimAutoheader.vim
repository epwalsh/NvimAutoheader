" =============================================================================
" File Name:     NvimAutoheader.vim
" Author:        Evan Pete Walsh
" Contact:       epwalsh10@gmail.com
" Creation Date: 2016-06-16
" Last Modified: 2016-06-17 18:58:19
" LICENSE:       The MIT License
"
"    Copyright (c) 2016 Evan Pete Walsh
"
"    Permission is hereby granted, free of charge, to any person obtaining a 
"    copy of this software and associated documentation files (the "Software"), 
"    to deal in the Software without restriction, including without limitation 
"    the rights to use, copy, modify, merge, publish, distribute, sublicense, 
"    and/or sell copies of the Software, and to permit persons to whom the 
"    Software is furnished to do so, subject to the following conditions:
"    
"    The above copyright notice and this permission notice shall be included in 
"    all copies or substantial portions of the Software.
"    
"    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
"    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
"    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
"    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
"    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
"    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
"    DEALINGS IN THE SOFTWARE.
"    
" =============================================================================


if !has('nvim') || !has('python')
    echohl Error | echomsg 'NvimAutoheader requires python and neovim' | echohl None
endif


function! NvimAutoheader#activate_autoheader()
    augroup NvimAutoheader
        autocmd!
        autocmd BufNewFile *.* call InsertHeader()
        autocmd BufWritePre,FileWritePre *.* call Update_header()
    augroup END 
endfunction
