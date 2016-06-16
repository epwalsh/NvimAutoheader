import neovim


@neovim.plugin
class Main(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.function('DoItPython')
    def doItPython(self, args):
        self.nvim.command('echom "hello"')

    @neovim.autocmd('FileWritePost', pattern='*.*')
    def on_write(self):
        self.nvim.command('echom "Hello there!"')

    @neovim.autocmd('BufWritePost', pattern='*.*')
    def on_write2(self):
        self.nvim.command('echom "hello there!"')
