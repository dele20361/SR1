import struct

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #1 word
    return struct.pack('=h', w)

def dword(d):
    #2 word
    return struct.pack('=l', d)

def color(r, g, b):
    '''
        Función para crear un color.
        La imagen se pone en bgr (o sea al revés).
        Se multiplica para pasarle de parámetro un valor de 0 a 1.
    '''
    return bytes([int(b * 255),
                  int(g * 255),
                  int(r * 255)])

class Renderer(object):
    def __init__(self, w, h):
        '''
            h: alto
            w: ancho
        '''
        self.width = w
        self.height = h
        self.clearColor = color(0,0,0) # Color predeterminado
        self.currColor = color(1,1,1)

        self.glViewport(0, 0, self.width, self.height) #Viewport predeterminado (del tamaño de la window)
        self.glClear()


    def glViewport(self, posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height


    def glClearColor (self, r, g, b):
        self.clearColor = color(r,g,b)

    def glColor (self, r, g, b):
        self.currColor = color(r,g,b) 

    def glClearViewport (self, clr=None):
        for x in range(self.vpX, self.vpX + self.vpWidth):
            for y in range(self.vpY, self.vpY + self.vpHeight):
                self.glPoint(x,y,clr)

    # Array de pixeles
    def glClear(self):
        '''
            Para determinar el color del fondo. 
            Borra todos lo que está en la pantalla.
            Esto se hace para poder crear los arrays de los pixeles.
        '''
        # Array de pixeles
        self.pixels = [[self.clearColor for y in range(self.height)]
                        for x in range (self.width)] # Array de ancho x altura, list comprehension

    def glPoint (self, x, y, clr = None):
        '''
            Función para trazar un punto en la pantalla con cordenadas
        '''
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y] = clr or self.currColor # Falta validar que x y y no supere el tamaño

    def glPoint_vp(self, ndcX, ndcY, clr = None):
        '''
            Función para trazar un punto en la pantalla con coordenadas normalizadas.
        '''
        if ndcX < -1 or ndcX > 1 or ndcY < -1 or ndcY > 1:
            return

        x = (ndcX + 1) * (self.vpWidth / 2) + self.vpX
        y = (ndcY + 1) * (self.vpHeight / 2) + self.vpY

        x = int(x)
        y = int(y)

        self.glPoint(x, y, clr)

    # Función para crear el bitmap/frame buffer
    def glFinish (self, filename):
        '''
        BMP FILE ESQUEME
            File header: Se dan las propiedades de la imagen. 
            filename: El nombre del archivo
        '''
        # Escritura en bytes -> wb
        with open(filename, "wb") as file:

            # Crear el FILE HEADER
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            # Para decirle el tamaño del archivo en bytes.
            # Usualmente son 40 bytes (offset),
            # 14 del header
            # y luego lo de los colores que es w*h*3 por los 3 colores.
            file.write(dword( 14 + 40 + (self.width * self.height * 3))) 
            file.write(dword(0))
            file.write(dword(14 + 40))

            # Crear INFORMATION HEADER
            # Ocupa 40 bytes
            file.write(dword(40))
            file.write(dword(self.width)) 
            file.write(dword(self.height))
            file.write(word(1)) # Planes
            # bits por pixel. Cuanta memoria voy a ocupar por cada pixel.
            file.write(word(24)) # 24 bits por pixel
            file.write(dword(0)) # Compression
            file.write(dword(self.width * self.height * 3)) # Image size
            # El resto se pueden quedar vacías
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # COLOR TABLE
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])
