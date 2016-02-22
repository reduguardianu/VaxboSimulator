import gtk
import pyperclip

from ImageFileChooser import ImageFileChooser

from VaxboSimulatorLogic import VaxboSimulator
from math import floor

class VaxboSimulatorGUI(gtk.Window):

    def __init__(self):
        super(VaxboSimulatorGUI, self).__init__()
        self.connect("destroy", gtk.main_quit)
        self.set_size_request(200, 200)
        self.set_position(gtk.WIN_POS_CENTER)

        self.simulator = VaxboSimulator("data/vaxbo.png")
        self.simulator.findSlots()

        self.mainImage = gtk.Image()
        self.mainImage.show()
        self.add(self.mainImage)
        self.show()
        self.add_events(gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.SCROLL_MASK)

        self.connect("button-release-event", self.onClick)
        self.connect("scroll-event", self.onScroll)
        self.scale = 1

        self.refreshImage()
        self.selected_images = dict()

    def applyScale(self):
        original_width = self.mainImage.get_pixbuf().get_width()
        original_height = self.mainImage.get_pixbuf().get_height()

        scaled_pixbuf = self.original_pixbuf.scale_simple(int(self.original_pixbuf.get_width() * self.scale), int(self.original_pixbuf.get_height() * self.scale), gtk.gdk.INTERP_BILINEAR)

        self.mainImage.set_from_pixbuf(scaled_pixbuf)
        self.resize(self.mainImage.get_pixbuf().get_width(), self.mainImage.get_pixbuf().get_height())
        self.move(self.get_position()[0] + (original_width - scaled_pixbuf.get_width()) / 2, (original_height - scaled_pixbuf.get_height()) / 2)



    def onScroll(self, window, event):
        pixbuf = self.mainImage.get_pixbuf()
        if event.direction == gtk.gdk.SCROLL_UP:
            self.scale *= 1.1
        else:
            self.scale *= 0.9

        self.applyScale()

    def showFilePicker(self):
        fileChooser = ImageFileChooser("Choose photo", buttons=(gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        result = fileChooser.run()
        if result == gtk.RESPONSE_OK:
            self.simulator.fillSlot(self.selectedSlot, fileChooser.get_filename())
            self.refreshImage()
            self.selected_images[self.selectedSlot] = fileChooser.get_filename()
        fileChooser.destroy()

    def onClick(self, widget, event):
        self.selectedSlot = None
        x = event.x * 1/self.scale
        y = event.y * 1/self.scale
        for slot in self.simulator.slots:
            if slot[0] <= x and x <= slot[0] + slot[2] and slot[1] <= y and y <= slot[1] + slot[3]:
                self.selectedSlot = slot
                self.showFilePicker()



    def refreshImage(self):
        self.original_pixbuf = self.simulator.getOutputPixbuf()
        self.mainImage.set_from_pixbuf(self.original_pixbuf)
        self.applyScale()

if __name__ == "__main__":
    gui = VaxboSimulatorGUI()
    gtk.main()
    filelist = ""
    for image in gui.selected_images.values():
        filelist += "* " + image + "\n"
    pyperclip.copy(filelist)
