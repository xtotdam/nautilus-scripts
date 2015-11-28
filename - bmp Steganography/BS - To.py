#!/usr/bin/python2

from PIL import Image
import zlib
import math

def BShide(filename):
	source = open(filename, 'rb').read()
	compressed = zlib.compress(source, 9)
	complen = len(compressed)
	print 'Compress:', len(source), '-->', complen

	taillen = complen % 3
	# print 'tail size =', taillen, 'bytes'

	# tail handling
	tailwritten = True
	if taillen:
		tail = compressed[-taillen:] + '\0' * (3 - taillen)
		tailwritten = False

	# pixel number needed to fit data
	pixelnum = int(math.ceil(complen/3.))

	# image side size
	sidesize = int(math.ceil(math.sqrt(pixelnum)))
	print 'Image size:', sidesize, 'x', sidesize, '=', sidesize**2

	im = Image.new("RGB", (sidesize, sidesize), 'black')
	for y in xrange(sidesize):
		for x in xrange(sidesize):
			offset = y * sidesize + x
			try:
				im.putpixel((x,y),
					(ord(compressed[3 * offset]),
					 ord(compressed[3 * offset + 1]),
					 ord(compressed[3 * offset + 2])))
			except IndexError:
				if not tailwritten:
					im.putpixel((x,y), (ord(tail[0]), ord(tail[1]), ord(tail[2])))
					tailwritten = True
				pass

	imagename = filename + '.bmp'
	im.save(imagename)
	print '* Image name:', imagename

if __name__ == '__main__':

	import sys
	for fn in sys.argv[1:]:
		print '** Now working with', fn
		BShide(fn)

