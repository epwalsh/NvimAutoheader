" =============================================================================
" File Name:     NvimAutoheader.vim
" Author:        Evan Pete Walsh
" Contact:       epwalsh10@gmail.com
" Creation Date: 2016-06-16
" Last Modified: 2016-06-16 14:58:58
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
