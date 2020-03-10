#import tkinter as tk
#
#frame = tk.Tk()  #tkinter modülünden Tk sınıfı ile bir nesne oluşturduk
#frame.geometry('500x500')  #geometry method'dur
#
#print(dir(frame))
#frame.mainloop()
#frame.destroy()

#import tkinter as tk
#
#pencere = tk.Tk()
#
#def çıkış():
#    etiket['text'] = 'Elveda zalim dünya...'
#    düğme['text'] = 'Bekleyin...'
#    düğme['state'] = 'disabled'
#    pencere.after(2000, pencere.destroy)
#
#etiket = tk.Label(text='Merhaba Zalim Dünya')
#etiket.pack()
#
#düğme = tk.Button(text='Çık', command=çıkış)
#düğme.pack()
#
#pencere.protocol('WM_DELETE_WINDOW', çıkış)
#
#pencere.mainloop()

import tkinter as tk

class Pencere(tk.Tk):     #Tk sınıfını miras aldık
    def __init__(self):
        #super().__init__()
        tk.Tk.__init__(self)  #eğer birden fazla sınıf miras alınmıyorsa super init iş görür. ancak birden fazla sınıf miras alınmışsa istediğimiz öncelik sırasında göre sınıfları init edebiliriz, aksi takdirde super __init__ parantezdeki sıraya göre init edecektir
        self.protocol('WM_DELETE_WINDOW', self.çıkış)

        self.etiket = tk.Label(text='Merhaba Zalim Dünya')
        self.etiket.pack()

        self.düğme = tk.Button(text='Çık', command=self.çıkış)
        self.düğme.pack()

    def çıkış(self):
        self.etiket['text'] = 'Elveda zalim dünya...'
        self.düğme['text'] = 'Bekleyin...'
        self.düğme['state'] = 'disabled'
        self.after(2000, self.destroy)

pencere = Pencere()
pencere.mainloop()