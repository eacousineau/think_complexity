import CA
import numpy

class Drawer(object):
    """Drawer is an abstract class that should not be instantiated.
    It defines the interface for a CA drawer; subclasses of Drawer
    should implement draw, show and save.

    draw_array is a utility that is used by several implementations.
    """
    def __init__(self):
        msg = 'Drawer is an abstract type and should not be instantiated.'
        raise ValueError, msg

    def draw(self, ca):
        """draw a representation of cellular automaton (ca).
        This function generally has no visible effect."""
    
    def show(self):
        """display the representation on the screen, if possible"""

    def save(self, filename):
        """save the representation of the CA in (filename)"""
        
    def draw_array(self, a):
        """iterate through array (a) and draw any non-zero cells"""
        for i in xrange(self.rows):
            for j in xrange(self.cols):
                if a[i,j]:
                    self.cell(j, self.rows-i-1)



class PyLabDrawer(Drawer):

    def __init__(self):
        # we only need to import these modules if a PyLabDrawer
        # gets instantiated
        global pylab
        import pylab

    def draw(self, ca, start=0, end=None):
        """draw the CA using pylab.pcolor."""

        pylab.gray()
        a = ca.get_array(start, end)
        rows, cols = a.shape

        # flipud puts the first row at the top; 
        # negating it makes the non-zero cells black."""
        pylab.pcolor(-numpy.flipud(a))
        pylab.axis([0, cols, 0, rows])

        # empty lists draw no ticks
        pylab.xticks([])
        pylab.yticks([])

    def show(self):
        """display the pseudocolor representation of the CA"""
        pylab.show()

    def save(self, filename='ca.png'):
        """save the pseudocolor representation of the CA in (filename)."""
        pylab.savefig(filename)
    



class PILDrawer(Drawer):

    def __init__(self):
        # we only need to import these modules if a PILDrawer
        # gets instantiated
        global Image, ImageDraw, ImageTk, Gui
        import Image
        import ImageDraw
        import ImageTk
        import Gui
        

    def draw(self, ca, start=0, end=None):
        a = ca.get_array(start, end)
        self.rows, self.cols = a.shape
        self.csize = 4
        size = [self.cols * self.csize, self.rows * self.csize]

        self.image = Image.new(mode='1', size=size, color=255)
        self.gui = Gui.Gui()
        self.button = self.gui.bu(command=self.gui.quit, relief=Gui.FLAT)
        self.draw = ImageDraw.Draw(self.image)
        self.draw_array(numpy.flipud(a))

    def cell(self, i, j):
        size = self.csize
        color = 0
        x, y = i*size, j*size
        self.draw.rectangle([x, y, x+size, y+size], fill=color)

    def rectangle(self, x, y, width, height, outline=0):
        self.draw.rectangle([x, y, x+width, y+height], outline=outline)

    def show(self):
        self.tkpi = ImageTk.PhotoImage(self.image)
        self.button.config(image=self.tkpi)
        self.gui.mainloop()
 
    def save(self, filename='ca.gif'):
        self.image.save(filename)


class EPSDrawer(Drawer):
    def __init__(self):
        self.cells = []

    def draw(self, ca, start=0, end=None):
        a = ca.get_array(start, end)
        self.rows, self.cols = a.shape
        self.draw_array(a)

    def cell(self, i, j):
        self.cells.append((i,j))
        
    def print_cells(self, fp):
        for i, j in self.cells:
            fp.write('%s %s c\n' % (i, j))

    def print_head(self, fp):
        fp.write('%!PS-Adobe-3.0 EPSF-3.0\n')
        fp.write('%%%%BoundingBox: -2 -2 %s %s\n' % (self.cols+2, self.rows+2))

        size = .9
        fp.write('/c {\n')
        fp.write('   newpath moveto\n')
        fp.write('   0 %g rlineto\n' % size)
        fp.write('   %g 0 rlineto\n' % size)
        fp.write('   0 -%g rlineto\n' % size)
        fp.write('   closepath fill\n')
        fp.write('} def\n')

    def print_outline(self, fp):
        fp.write('newpath 0.1 setlinewidth 0 0 moveto\n')
        fp.write('0 %s rlineto\n' % self.rows)
        fp.write('%s 0 rlineto\n' % self.cols)
        fp.write('0 -%s rlineto\n' % self.rows)
        fp.write('closepath stroke\n')

    def print_tail(self, fp):
        fp.write('%%EOF\n')

    def show(self):
        pass

    def save(self, filename='ca.eps'):
        fp = open(filename, 'w')
        self.print_head(fp)
        self.print_outline(fp)
        self.print_cells(fp)
        self.print_tail(fp)

    


def main(script, rule=30, n=100, *args):
    rule = int(rule)
    n = int(n)

    ca = CA.CA(rule, n)

    if 'random' in args:
        ca.start_random()
    else:
        ca.start_single()

    ca.loop(n-1)

    if 'eps' in args:
        drawer = EPSDrawer()
    elif 'pil' in args:
        drawer = PILDrawer()
    else:
        drawer = PyLabDrawer()

    if 'trim' in args:
        drawer.draw(ca, start=n/2, end=3*n/2+1)
    else:
        drawer.draw(ca)

    drawer.show()
    drawer.save()

if __name__ == '__main__':
    import sys
    main(*sys.argv)
