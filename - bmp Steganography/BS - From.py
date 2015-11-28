#!/usr/bin/python2

from PIL import Image
import zlib
import itertools

def BSreveal(filename):
	im = Image.open(filename)
	sidesize = im.size[0]
	print 'Image size:', sidesize, 'x', sidesize, '=', sidesize**2

	data = (im.getpixel((x, y)) for y in xrange(sidesize) for x in xrange(sidesize))
	data = itertools.chain(*data)

	compressed = ''.join((chr(i) for i in data))
	unhiddendata = zlib.decompress(compressed)
	print 'Decompress:', len(compressed), '-->', len(unhiddendata)

	fn = filename[:-4].split('.')
	newfilename = fn[0] + '.extracted.' + '.'.join(fn[1:])
	print '* Restored file name:', newfilename

	with open(newfilename, 'wb') as f:
		f.write(unhiddendata)

if __name__ == '__main__':
	import sys
	for fn in sys.argv[1:]:
		print '** Now working with', fn
		BSreveal(fn)
