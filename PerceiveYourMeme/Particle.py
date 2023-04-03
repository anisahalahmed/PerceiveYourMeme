# An easter egg
from io import BytesIO

from PIL import Image

from .CONST import HEADERS, request

# I intentionally do this in one line.
url = "https://vignette.wikia.nocookie.net/marvelcinematicuniverse/images/0/03/Pym_Particles.png"
Image.open(BytesIO(request("GET", url, headers=HEADERS).data)).show()
