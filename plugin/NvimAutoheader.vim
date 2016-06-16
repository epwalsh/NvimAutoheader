" =============================================================================
" File Name:     NvimAutoheader.vim
" Author:        Evan Pete Walsh
" Contact:       epwalsh10@gmail.com
" Creation Date: 2016-06-16
" Last Modified: 2016-06-16 14:58:56
" =============================================================================


" if !has('nvim') || !has('python')
    " echohl Error | echomsg 'NvimAutoheader requires python and neovim' | echohl None
" endif

if !exists('g:NvimAutoheader')
    let g:NvimAutoheader = 1
endif

if g:NvimAutoheader
    if !exists('g:NvimAutoheader_author')
        let g:NvimAutoheader_author = ''
        " echo '[Autoheader] to set default author "let g:NvimAutoheader_author = "'
    endif
    if !exists('g:NvimAutoheader_contact')
        let g:NvimAutoheader_contact = ''
        " echo '[Autoheader] to set default contact "let g:NvimAutoheader_contact = "'
    endif
    if !exists('g:NvimAutoheader_website')
        let g:NvimAutoheader_website = ''
    endif
    call NvimAutoheader#activate_autoheader()
    " augroup NvimAutoheader
        " autocmd!
        " autocmd BufNewFile *.* call InsertHeader()
        " autocmd BufWritePre,FileWritePre *.* call Update_header()
    " augroup END 
endif
