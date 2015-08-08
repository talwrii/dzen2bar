# dzen2bar

A reimplementation of i3bar that uses dzen2 for output. Also adds support for custom properties that are not supported by i3. The intended use case is adding dzen2 features to your i3bar settings, while still being able to use i3bar tooling (i3pystatus, i3status etc).

## Usage

The easiest setup is probably to use i3cat

* Install https://github.com/vincent-petithory/i3cat
* Set up your i3cat to include some dzen2 output

        # cat ~/.i3/i3cat.conf
        python3 ~/.i3/status.py
        i3cat encode '^i(/usr/share/pixmaps/python.xpm)' --name python

* Feed this through dzen2bar.py

         i3cat | python -m dzen2bar 'Courier'

## Caveats

* The `min_width` and `pango` properties are not supported - though they can be ignored with appropriate command line arguments.
* No attempt is made to escape dzen2 formatting markup. This could be considered a feature.

## Alternatives

* *i3-wmbar* was the reference implementation of *i3bar*. This is written in perl and supports output to dzen2.

* There exists a patch to i3bar that supports xpm images. For my use cases, I was not keen on maintaining a patched version of a C project for my own use.
