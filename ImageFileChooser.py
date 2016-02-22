import gtk

class ImageFileChooser(gtk.FileChooserDialog):
    def __init__(self, title, buttons):
        super(ImageFileChooser, self).__init__(title, buttons=buttons)
        self.preview = gtk.Image()
        self.set_preview_widget(self.preview)
        self.connect("selection-changed", self.updatePreview)


    def updatePreview(self, data):
        if self.get_preview_filename() is None:
            return
        pixbuf = gtk.gdk.pixbuf_new_from_file(self.get_preview_filename())
        width = None
        height = None
        if pixbuf.get_width() > pixbuf.get_height():
            width = 200
            height = 200 * pixbuf.get_height()/pixbuf.get_width()
        else:
            height = 200
            width = 200 * pixbuf.get_width()/pixbuf.get_height()

        scaled_buf = pixbuf.scale_simple(width,height,gtk.gdk.INTERP_BILINEAR)
        self.preview.set_from_pixbuf(scaled_buf)
