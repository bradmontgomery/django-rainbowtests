"""
This code was shamelessly stolen from Fabric:
https://github.com/fabric/fabric/blob/master/fabric/colors.py

-------------------------------------------------------------------------------

Copyright (c) 2009, Christian Vest Hansen and Jeffrey E. Forcier
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
-------------------------------------------------------------------------------

Functions for wrapping strings in ANSI color codes.

Each function within this module returns the input string ``text``, wrapped
with ANSI color codes for the appropriate color.

For example, to print some text as green on supporting terminals::

    from fabric.colors import green

    print(green("This text is green!"))

Because these functions simply return modified strings, you can nest them::

    from fabric.colors import red, green

    print(red("This sentence is red, except for " + \
          green("these words, which are green") + "."))

If ``bold`` is set to ``True``, the ANSI flag for bolding will be flipped on
for that particular invocation, which usually shows up as a bold or brighter
version of the original color on most terminals.
"""


def _wrap_with(code):

    def inner(text, bold=False):
        c = code
        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)
    return inner

red = _wrap_with('31')
green = _wrap_with('32')
yellow = _wrap_with('33')
blue = _wrap_with('34')
magenta = _wrap_with('35')
cyan = _wrap_with('36')
white = _wrap_with('37')
