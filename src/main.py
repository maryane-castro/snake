from PIL import Image

img = Image.open("dragon.png")

#exibe ela
img.show()

#amplia para 800x600


novaresolucao = ()

img2 = img.resize((800,600))
img2.show()

#amplia com antialiasing
img3 = img.resize((800,600),Image.ANTIALIAS)
img3.show()