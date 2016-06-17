" =============================================================================
" File Name:     NvimAutoheader.vim
" Author:        Evan Pete Walsh
" Contact:       epwalsh10@gmail.com
" Creation Date: 2016-06-16
" Last Modified: 2016-06-17 00:27:48
" =============================================================================


" if !has('nvim') || !has('python')
    " echohl Error | echomsg 'NvimAutoheader requires python and neovim' | echohl None
" endif

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
    if !exists('g:NvimAutoheader_width')
        let g:NvimAutoheader_width = 80
    endif
    if !exists('g:NvimAutoheader_license_verbose')
        let g:NvimAutoheader_license_verbose = 0
        if !exists('g:NvimAutoheader_license')
            let g:NvimAutoheader_license = ''
        endif
    endif

    call NvimAutoheader#activate_autoheader()
endif
