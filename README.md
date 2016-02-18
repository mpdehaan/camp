CAMP - Computer Aided Music Production
======================================

CAMP is a music composition project that attempts to solve some fun problems:

   * How do we teach a computer to be a cybernetic extension of a songwriter or composer?
   * How can we buck the trend of non-listenable computer music by mixing in lots of interesting tricks from music theory and songwriting?
   * How do we teach computers to play jazz?
   * Are there better ways for describing a performance in ASCII than music notation?
   * What would 'music as code' (see "infrastructure as code") look like?

Many of these things are obviously ambitious.  CAMP is an ever-evolving project, but it is also a set of building blocks that are usable for realtime music and theory work now.
As such, it can create smaller things along the way.

Get a VST/AU soft synth, a machine with Python on it, and let's dig in.

Examples
========

See the examples/ directory for lots of fun stuff!

Goals
=====

Stage 1 (mostly complete):

   * a python-based, intuitive music theory library, enabling "music as code"
   * an implementation that makes sense musically, that uses musical terms and  higher level objects where needed to make things easy to follow
   * scale awareness at the forefront with ability to use roman numeral notation for chords, etc
   * a library suitable as a basis for theory-backed algorithmic composition programs
   * tools that enable composition at faster speeds, inspired by trackers but evolved from them

Stage 2 (in progress) - see the API example above:

   * a system that can represent a mesh network of improvising but conducted "musicians"
   * a library of usable mutators to slice, dice, and evolve musical patterns
   * inspirations: Real life Jazz, the Reactable at the Museum of the Science and Industry, etc
   * endless-composition genre-shifting program  suitable for never ending songs that also remain interesting

Stage 3 (pending and orthogonal):

   * a friendly entry format for rapid transcription of scores across multiple tracks, inspired by classic step sequencers, and usuable by non-programmers
   * inspirations: the Elektron Monomachine, the Sequentix Cirklon, etc.
   * a way to allow randomness and chaos to influence the compositions
   * easy to describe automation of synth parameters (filter cutoffs, wub wub, etc) 

Design Goals:

   * easy to understand code
   * ease of setup
   * some independence from low level MIDI implementations, so we're not dependent on some library continuing to work, but enable both realtime MIDI, MIDI output, and notation

These features might not all be used at the same time or even be 100% compatible, but will grow and evolve out of a common base.

License
=======

Apache 2

Mailing List
============

If you want to get involved with the project, we have a Google Group.

On topic: Ideas, Code discussions, Troubleshooting,  Bug Reports, Sharing things you've built with CAMP, Q&A.

* https://groups.google.com/forum/#!forum/camp-python-music


Notes
=====

   * The tests probably explain the API best at this point, see tests/band.py and other files
   * API is super subject to change.
   * Contributors should join the mailing list at https://groups.google.com/forum/#!topic/camp-python-music - to avoid frustration, duplicate work, and API breakage, I highly suggest talking about what you are going to be doing it.
   * The issue tracker is disabled.  Fix something via a pull request or ask a question on the mailing list.
   * If you use CAMP for something interesting, I'd love to hear about it, let me know!

Setup: OS X
===========

It's recommended you target some soft synths running inside a Digital Audio Workstation program (DAW) or standalone.  

Initial testing in the early days of this program were done against Native Instrument's Absynth and Reaper.  These are prety friendly to set up
MIDI wise.

For the program itself, software dependencies:

    # first setup homebrew
    brew install python3
    pip3 install -r requirements.txt

Open "Audio/MIDI Setup" on OS X, pick "Window / Open MIDI  Studio" and click on the IAC Driver Block.  Pick "Enabled" and make sure
there are some MIDI ports there.

To make sure CAMP is using the right bus, run the following:

    PYTHONPATH=. python3 examples/00_ports_and_setup.py

Which will explain how to select a different bus if needed, and will make sure you are using the right one.

Then:
 
   make tests

If you skip the IAC step the tests may fail. 

If your IAC driver is not the *SECOND* MIDI port, the system may also fail.  This is because things take a port number.  I need to make
this read in via en environment variable.  Short term, hack camp/playback/realtime.py if this doesn't work, and change this line:

        midi_out.open_port(1)

If you are using Logic, Logic is by default idiotic when it comes to MIDI and multi-track recording.  In Logic X, go to File > Project Settings > Recording
and be sure the "Auto Demix" option is checked.  Then, one each channel strip, assign a MIDI channel that is not "ALL".  You will then want to arm all tracks
for recording before running the program.

If you have problems with this step (or want to share Windows/Linux tips), stop by the mailing list!

Author
======

   * CAMP is written by Michael DeHaan (michael.dehaan@gmail.com)

