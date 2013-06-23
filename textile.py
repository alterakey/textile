# -*- coding: utf-8 -*-
# textile.py: Textile indexer/finder.
# Copyright (C) 2013 Takahiro Yoshimura <altakey@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import subprocess
import sys
import regex

class Decoder(object):
  coding_list = ('utf-8', 'euc-jp', 'cp932', 'ascii', 'utf-16')

  def decode(self, line):
    for coding in self.coding_list:
      try:
        return line.decode(coding)
      except UnicodeDecodeError:
        pass
    else:
      return line.decode('utf-8', errors='replace')


class Index(object):
  include_list = ('*.php', '*.js', '*.css', '*.xml', '*.html', '*.py', '*.as')
  exclude_list = ('.git', '.svn', 'CVS')

  def update(self, root):
    self.data = ''
    decoder = Decoder()
    try:
      proc = subprocess.Popen("grep -niEHR '.' %s %s %s" % (' '.join("--include='%s'" % c for c in self.include_list), ' '.join("--exclude='%s'" % c for c in self.exclude_list), root), shell=True, stdout=subprocess.PIPE)
      for block in proc.stdout:
        self.data = self.data + decoder.decode(block)
    finally:
      proc.terminate()
      proc.wait()


index = Index()

class InteractiveShell(object):
  def __init__(self, in_, out_):
    self.in_ = in_
    self.out_ = out_

  def serve_forever(self):
    decoder = Decoder()
    while True:
      self._print(u'textile> ', raw=True)
      line = decoder.decode(self.in_.readline(65536))
      if not line:
        break
      else:
        line = regex.sub(u'^\s*|\s*$', u'', line, regex.V1)
        if line:
          self._serve(line)

  def _print(self, msg, raw=False):
    self.out_.write(msg.encode('utf-8'))
    if not raw:
      self.out_.write("\n")

  def _serve(self, cmdline):
    args = cmdline.split(' ')
    try:
      dict(help=self._help, update=self._update, find=self._find)[args[0]](*args[1:])
    except KeyError:
      self._print('textile: "%s": command unknown' % args[0])

  def _help(self, *args):
    self._print(u'''\
help, available commands are:
- none.\
''')

  def _update(self, *args):
    global index
    for path in args:
      self._print(u'updating with %s ...' % path, raw=True)
      index.update(path)
      self._print(u' (%d bytes)' % len(index.data))
    self._print(u'... done')

  def _find(self, *args):
    global index
    try:
      for match in regex.finditer(u'^.+?:\d+?:.*%s.*$' % args[0], index.data, regex.MULTILINE | regex.IGNORECASE | regex.V1, concurrent=True):
        self._print(match.group(0))
    except sre_constants.error, e:
      print

if __name__ == '__main__':
  InteractiveShell(sys.stdin, sys.stdout).serve_forever()
