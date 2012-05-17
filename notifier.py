from pyosd import *
def osd(message):
    p = osd()
    p.set_align(ALIGN_CENTER)
    p.display(message)
    
if __name__ == '__main__':
    osd('Earthquake alarm')