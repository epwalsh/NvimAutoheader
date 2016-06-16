
" The VimL/VimScript code is included in this sample plugin to demonstrate the
" two different approaches but it is not required you use VimL. Feel free to
" delete this code and proceed without it.


function DoItVimL()
    echo "DoItVimL"
endfunction


augroup Nvim-autoheader
    autocmd!
    " autocmd BufWritePre,FileWritePre *.* execute DoItPython()
    " autocmd BufWritePost,FileWritePost *.* execute DoItPython()
    " autocmd BufWritePost,FileWritePost *.* echom "hello"
augroup END 
