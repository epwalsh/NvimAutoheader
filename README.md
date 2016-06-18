# NvimAutoheader

[![Packagist](https://img.shields.io/packagist/l/doctrine/orm.svg)](https://github.com/epwalsh/NvimAutoheader/blob/master/LICENSE)

Automatic header management for [Neovim](https://github.com/neovim/neovim). Currently
supported filetypes:
- Python
- R
- C / C++
- Shell
- VimL
- Javascript
- Java
- Julia
- Go
- Ruby
- PHP

![](doc/NvimAutoheader_main.gif)

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

### Other features

To automatically insert an open source license into the header of new files:

```vim
let g:NvimAutoheader_license = 'MIT'      # Automatically add MIT license
let g:NvimAutoheader_license_verbose = 1  # Put full license text into header
```

To insert a full license into a file use the following command:

```vim
HeaderLicense MIT
```

Current licenses that are supported:
- MIT
- Apache-2.0
- GPL
- BSD

If NvimAutoheader doesn't have a copy of the full license that you wish to insert,
you can add a file to ```plugin/licenses/[Name of license]``` with the text and NvimAutoheader will insert that header when you call

```vim
HeaderLicense [Name of license]
```

To insert an arbitrary file into the header:

```vim
HeaderAppend [path to file]
```
