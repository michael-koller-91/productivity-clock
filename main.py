import tkinter as tk
import core
import menu


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title('Productivity Clock')

        self.core = core.Core(self)
        self.core.grid()
        # keyboard focus
        self.core.focus_set()

        self.menu = menu.Menu(self)
        self.menu.grid()

        # place window in bottom right corner
        self.parent.update()
        wh = self.core.winfo_height()
        ww = self.core.winfo_width()
        sw = self.parent.winfo_screenwidth() - ww - 15
        sh = self.parent.winfo_screenheight() - wh - 80
        self.parent.geometry('{}x{}+{}+{}'.format(ww, wh, sw, sh))
        self.parent.resizable(0, 0)


def main():
    root = tk.Tk()
    MainApplication(root).pack(expand=True)
    root.mainloop()


if __name__ == '__main__':
    main()
