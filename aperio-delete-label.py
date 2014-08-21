#!/usr/bin/python
#
#  Delete the label image from an Aperio SVS file.
#
#  Copyright (c) 2012-2013 Carnegie Mellon University
#  All rights reserved.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of version 2 of the GNU General Public License as
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110-1301 USA.
#

import string
import struct
import sys

ASCII = 2
SHORT = 3
LONG = 4
LONG8 = 16

IMAGE_DESCRIPTION = 270
STRIP_OFFSETS = 273
STRIP_BYTE_COUNTS = 279

class TiffFile(file):
    def __init__(self, path):
        file.__init__(self, path, 'r+b')

        # Check header, decide endianness
        endian = self.read(2)
        if endian == 'II':
            self._fmt_prefix = '<'
        elif endian == 'MM':
            self._fmt_prefix = '>'
        else:
            raise IOError('Not a TIFF file')

        # Check TIFF version
        self._bigtiff = False
        version = self.read_fmt('H')
        if version == 42:
            pass
        elif version == 43:
            self._bigtiff = True
            magic2, reserved = self.read_fmt('HH')
            if magic2 != 8 or reserved != 0:
                raise IOError('Bad BigTIFF header')
        else:
            raise IOError('Not a TIFF file')

        # Read directories
        self.directories = []
        while True:
            in_pointer_offset = self.tell()
            directory_offset = self.read_fmt('Z')
            if directory_offset == 0:
                break
            self.seek(directory_offset)
            self.directories.append(TiffDirectory(self, in_pointer_offset))

    def _convert_format(self, fmt):
        # Format strings can have special characters:
        # y: 16-bit   signed on little TIFF, 64-bit   signed on BigTIFF
        # Y: 16-bit unsigned on little TIFF, 64-bit unsigned on BigTIFF
        # z: 32-bit   signed on little TIFF, 64-bit   signed on BigTIFF
        # Z: 32-bit unsigned on little TIFF, 64-bit unsigned on BigTIFF
        if self._bigtiff:
            fmt = fmt.translate(string.maketrans('yYzZ', 'qQqQ'))
        else:
            fmt = fmt.translate(string.maketrans('yYzZ', 'hHiI'))
        return self._fmt_prefix + fmt

    def fmt_size(self, fmt):
        return struct.calcsize(self._convert_format(fmt))

    def read_fmt(self, fmt, force_list=False):
        fmt = self._convert_format(fmt)
        vals = struct.unpack(fmt, self.read(struct.calcsize(fmt)))
        if len(vals) == 1 and not force_list:
            return vals[0]
        else:
            return vals

    def write_fmt(self, fmt, *args):
        fmt = self._convert_format(fmt)
        self.write(struct.pack(fmt, *args))


class TiffDirectory(object):
    def __init__(self, fh, in_pointer_offset):
        self.in_pointer_offset = in_pointer_offset
        self.entries = {}
        count = fh.read_fmt('Y')
        for _ in range(count):
            entry = TiffEntry(fh)
            self.entries[entry.tag] = entry
        self.out_pointer_offset = fh.tell()


class TiffEntry(object):
    def __init__(self, fh):
        self.start = fh.tell()
        self.tag, self.type, self.count, self.value_offset = \
                fh.read_fmt('HHZZ')
        self._fh = fh

    def value(self):
        if self.type == ASCII:
            item_fmt = 'c'
        elif self.type == SHORT:
            item_fmt = 'H'
        elif self.type == LONG:
            item_fmt = 'I'
        elif self.type == LONG8:
            item_fmt = 'Q'
        else:
            raise ValueError('Unsupported type')

        fmt = '%d%s' % (self.count, item_fmt)
        len = self._fh.fmt_size(fmt)
        if len <= self._fh.fmt_size('Z'):
            # Inline value
            self._fh.seek(self.start + self._fh.fmt_size('HHZ'))
        else:
            # Out-of-line value
            self._fh.seek(self.value_offset)
        items = self._fh.read_fmt(fmt, force_list=True)
        if self.type == ASCII:
            if items[-1] != '\0':
                raise ValueError('String not null-terminated')
            return ''.join(items[:-1])
        else:
            return items


def delete_aperio_label(filename):
    with TiffFile(filename) as fh:
        for directory in fh.directories:
            # Check ImageDescription
            try:
                desc = directory.entries[IMAGE_DESCRIPTION].value()
            except KeyError:
                continue
            if not desc.startswith('Aperio'):
                # Not an Aperio directory
                continue
            lines = desc.splitlines()
            if len(lines) < 2 or not lines[1].startswith('label '):
                # Not the label
                continue

            # Get strip offsets/lengths
            try:
                offsets = directory.entries[STRIP_OFFSETS].value()
                lengths = directory.entries[STRIP_BYTE_COUNTS].value()
            except KeyError:
                raise IOError('Label is not stripped')

            # Wipe strips
            for offset, length in zip(offsets, lengths):
                fh.seek(offset)
                fh.write('\0' * length)

            # Delete directory
            fh.seek(directory.out_pointer_offset)
            out_pointer = fh.read_fmt('Z')
            fh.seek(directory.in_pointer_offset)
            fh.write_fmt('Z', out_pointer)

            # Done
            break
        else:
            raise IOError("Couldn't find Aperio label directory")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >>sys.stderr, 'Usage: %s <svs-file>...' % sys.argv[0]
        sys.exit(2)
    exit_code = 0
    for filename in sys.argv[1:]:
        try:
            delete_aperio_label(filename)
        except Exception, e:
            print >>sys.stderr, '%s: %s' % (filename, str(e))
            exit_code = 1
    sys.exit(exit_code)
