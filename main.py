import tkinter as tk
import core
# import menu


class MainApplication(tk.Frame):
    def __init__(self, parent, hours, minutes, outfile, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title('Productivity Clock')

        self.core = core.Core(self, hours, minutes, outfile)
        self.core.grid()
        # keyboard focus
        self.core.focus_set()

        # self.menu = menu.Menu(self)
        # self.menu.grid()

        # place window in bottom right corner
        self.parent.update()
        wh = self.core.winfo_height()
        ww = self.core.winfo_width()
        sw = self.parent.winfo_screenwidth() - ww - 15
        sh = self.parent.winfo_screenheight() - wh - 80
        self.parent.geometry('{}x{}+{}+{}'.format(ww, wh, sw, sh))
        self.parent.resizable(0, 0)


def main(hours, minutes, outfile):
    root = tk.Tk()
    MainApplication(root, hours, minutes, outfile).pack(expand=True)
    root.mainloop()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog='Productivity Clock')
    parser.add_argument('--hours', type=int, default=2)
    parser.add_argument('--minutes', type=int, default=30)
    parser.add_argument('--outfile', type=str, default='clock')
    pargs = parser.parse_args()

    main(pargs.hours, pargs.minutes, pargs.outfile)
