" =============================================================================
" File Name:     NvimAutoheader.vim
" Author:        Evan Pete Walsh
" Contact:       epwalsh10@gmail.com
" Creation Date: 2016-06-16
" Last Modified: 2016-06-16 13:45:27
" =============================================================================


" if !has('nvim') || !has('python')
    " echohl Error | echomsg 'NvimAutoheader requires python and neovim' | echohl None
" endif

" function! NvimAutoheader#activate_autoheader()
    " augroup NvimAutoheader
        " autocmd!
        " autocmd BufNewFile *.* execute InsertHeader()
        " " autocmd BufWritePre,FileWritePre *.* execute Update_header()
    " augroup END 
" endfunction
