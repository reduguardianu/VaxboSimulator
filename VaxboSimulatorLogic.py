from PIL import Image
import gtk
import StringIO

class VaxboSimulator:

    def __init__(self, filename):
        self.image = Image.open(filename)
        self.image.convert("RGBA")
        self.output = self.image.copy()


    def findSlots(self):
        pixels = self.image.load()

        slotCorners = []
        for i in range(0, self.image.size[0]):
            for j in range(0, self.image.size[1]):
                if pixels[i, j] == (255, 0, 0, 255): #red pixel
                    slotCorners.append((i, j))

        self.slots = []
        for corner in slotCorners:
            colIndex = corner[0]
            while (colIndex < self.image.size[0] and pixels[colIndex + 1, corner[1]][3] == 0):
                colIndex += 1
            rowIndex = corner[1]
            while (rowIndex + 1 < self.image.size[1] and pixels[corner[0], rowIndex + 1][3] == 0):
                rowIndex += 1

            self.slots.append((corner[0], corner[1], colIndex - corner[0], rowIndex - corner[1]))


    def fillSlot(self, slot, photo):
        photoImage = Image.open(photo).copy()
        photoImage = photoImage.resize((slot[2], slot[3]))
        self.output.paste(photoImage, (slot[0], slot[1]))

    def getOutputPixbuf(self):
        file1 = StringIO.StringIO()
        self.output.save(file1, "ppm")
        contents = file1.getvalue()
        file1.close()
        loader = gtk.gdk.PixbufLoader("pnm")
        loader.write(contents, len(contents))
        pixbuf = loader.get_pixbuf()
        loader.close()
        return pixbuf

if __name__ == "__main__":
    sim = VaxboSimulator("data/vaxbo.png")
    sim.findSlots()
    photos = ["testPhotos/1.JPG", "testPhotos/2.JPG",  "testPhotos/3.JPG", "testPhotos/4.JPG", "testPhotos/5.JPG", "testPhotos/6.JPG", "testPhotos/7.JPG", "testPhotos/8.JPG"]
    i = 0
    for slot in sim.slots:
        sim.fillSlot(slot, photos[i])
        i += 1
    sim.output.save("output.png")
