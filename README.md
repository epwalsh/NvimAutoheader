# NvimAutoheader

[![Packagist](https://img.shields.io/packagist/l/doctrine/orm.svg)](https://github.com/epwalsh/NvimAutoheader/blob/master/LICENSE)

Automatic header management for [Neovim](https://github.com/neovim/neovim)

![](http://epwalsh.com/images/NvimAutoheader_main.gif)

### Install

The easiest way to install is with your favorite plugin manager. For me, that's 
[Vundle](https://github.com/VundleVim/Vundle.vim). Just add the necessary lines 
to your ```.vimrc``` / ```init.vim```.

```vim
filetype off

set rtp+=~/.config/nvim/bundle/Vundle.vim
call vundle#begin("~/.config/nvim/bundle/")

Bundle 'gmarik/Vundle.vim'
" your other plugins ...

Bundle 'epwalsh/NvimAutoheader'

call vundle#end()
filetype plugin indent on
```

This plugin depends on Python, so you also have to run ```:UpdateRemotePlugins```
and then restart Neovim.


### Setup

To set the default author and contact information, add the following lines to 
your ```.vimrc```:

```vim
let g:NvimAutoheader_author = 'your name'
let g:NvimAutoheader_contact = 'your email'
let g:NvimAutoheader_website = 'your website'
```

If you do not set these variables, NvimAutoheader will not include these lines in the 
header.

To disable automatically inserting headers into new files: 

```vim
let g:NvimAutoheader = 0
```
