#!/usr/bin/python
# -*- coding: utf-8 -*-
# gen.py is copyright (C) 2008-2012, Dave Crossland (dave@understandingfonts.com)
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are met:
#
#   Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
#   The name of the author may not be used to endorse or promote products
#   derived from this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED
#   WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#   MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
#   EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""A FontForge plug-in to generate UFO masters from layers.
   Copy to ~/.FontForge/python/ and then find "Generate Masters" in the Tools menu.
"""

# XXX
# font.randomText(script[,language])
# where script and language are OpenType tags expressed as strings
# font.randomText("latn","ENG ")

import fontforge, sys, os, time, shutil, tempfile, subprocess, fileinput



def geMaster(myFont):
  myFont.save()
  mastLayer1 = 'Fore'
  s1 = fontforge.askString("Export layers to masters", "Name of the Light Master layer ?", str(mastLayer1))
  mastLayer1 = s1
  mastLayer2 = 'Back'
  s2 = fontforge.askString("Export layers to masters", "Name of the ExtraBold Master layer ?", str(mastLayer2))
  mastLayer2 = s2
  fontName =  myFont.fontname
  fontforge.logWarning("Saved master file")
  myFont.generate(fontName + '_1.otf', layer= mastLayer1)
  fontforge.logWarning("Generated Light from Foreground")
  myFont.generate(fontName + '_0.otf',layer= mastLayer1)
  fontforge.logWarning("Generated ExBld from mastLayer1")




def genMast(junk,glyph):
  """Generate Masters"""
  myFont = fontforge.activeFont()
  geMaster(myFont)
  fontforge.logWarning("All done!")


if fontforge.hasUserInterface():
  keyShortcut="Ctl+Shft+n"
  fontforge.registerMenuItem(genMast,None,None,("Font","Glyph"),keyShortcut,"Generate Masters from layers ");
  keyShortcut="Ctl+Shft+p"
