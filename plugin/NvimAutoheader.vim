" =============================================================================
" File Name:     NvimAutoheader.vim
" Author:        Evan Pete Walsh
" Contact:       epwalsh10@gmail.com
" Creation Date: 2016-06-16
" Last Modified: 2017-06-15 17:41:24
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


if !exists('g:NvimAutoheader')
    let g:NvimAutoheader = 1
endif

if g:NvimAutoheader
    let g:NvimAutoheader_location = expand("<sfile>:h")

    if !exists('g:NvimAutoheader_author')
        let g:NvimAutoheader_author = ''
    endif
    if !exists('g:NvimAutoheader_contact')
        let g:NvimAutoheader_contact = ''
    endif
    if !exists('g:NvimAutoheader_website')
        let g:NvimAutoheader_website = ''
    endif
    if !exists('g:NvimAutoheader_organization')
        let g:NvimAutoheader_organization = ''
    endif
    if !exists('g:NvimAutoheader_width')
        let g:NvimAutoheader_width = 80
    endif
    if !exists('g:NvimAutoheader_append_path')
        let g:NvimAutoheader_append_path = ''
    endif
    if !exists('g:NvimAutoheader_license_verbose')
        let g:NvimAutoheader_license_verbose = 0
        if !exists('g:NvimAutoheader_license')
            let g:NvimAutoheader_license = ''
        endif
    endif

    call NvimAutoheader#activate_autoheader()
endif
