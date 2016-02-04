CAMP - Computer Aided Music Production
======================================

CAMP is a music composition project.

Goals are to provide:

   * a pythonic and intuitive music theory library, enabling "music as code"
   * tools that enable composition at faster speeds, inspired by trackers but evolved from them
   * scale awareness at the forefront with ability to use roman numeral notation for chords, etc
   * a library suitable as a basis for theory-backed algorithmic composition programs
   * pluggable output modes so we're not dependent on some library continuing to work, but enable both realtime MIDI, MIDI output, and notation
   * a friendly entry format for rapid transcription of scores across multiple tracks, inspired by classic step sequencers
   * a library of usable mutators to slice, dice, and evolve musical patterns
   * easy to describe automation of synth parameters (filter cutoffs, wub wub, etc) 
   * endless-composition genre-shifting program  suitable for never ending songs that also remain interesting

License
=======

Apache 2

Notes
=====

   * The tests probably explain the API best at this point
   * There's much to do
   * API is super subject to change.
   * No pull requests or tickets just yet please.
   * If you use CAMP for something interesting, I'd love to hear about it, let me know!


Setup
=====

For OS X:

    brew install python3
    pip3 install -r requirements.txt

Open "Audio/MIDI Setup" and click on the IAC Driver Block.  Pick "Enabled".  

Then:
 
   make tests

If you skip the IAC step the tests may fail. 

Author
======

   * CAMP is written by Michael DeHaan (michael.dehaan@gmail.com)

