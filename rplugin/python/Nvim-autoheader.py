import neovim


@neovim.plugin
class Autoheader(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.function('DoItPython')
    def doItPython(self, args):
        ext = self.nvim.eval('expand("%:s")')
        self.nvim.command('echom "hello ' + ext + '"')

    @neovim.autocmd('FileWritePost', pattern='*.*')
    def on_write(self):
        self.nvim.command('echom "Hello there!"')

    @neovim.autocmd('BufWritePost', pattern='*.*')
    def on_write2(self):
        self.nvim.command('echom "hello there!"')
