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

API Example
===========

Here's some early mesh-network inspired stuff, from a version of tests/band.py:

        output = Performance(bpm=120, stop_seconds=10)
        scale1 = scale("c6 major")
        scale2 = scale("c6 minor")

        source = ScaleSource(scales=[ dict(scale=scale1, beats=7), dict(scale=scale2, beats=7) ])
        subdivide = Subdivide(splits=[4])
        roman = Roman(symbols="1 2 3 4 I IV V iii".split(), channel=1)

        follower = ScaleFollower(lengths=[ 7 ])
        chordify = Chordify(types=[ 'power' ])
        shift = Transpose(octaves=[-3], channel=2)

        source.chain([subdivide, roman, output])
        source.chain([follower, chordify, shift, output])

        conductor = Conductor(signal=[source], performance=output)
        conductor.start()

This isn't really meant to be a Top 40 song, but it's illustrative of the API features.

The performance starts in one scale, the C Major scale based around the 6th octave for 7 beats.  After 7 beats
it goes down to C6 minor.

There are really two instruments involved.  While a beat is a quarter note, the first musician is playing sixteenths, repeating
a pattern.  The pattern is the first four notes in the scale, followed by the first, fourth, and fifth major chord.  Then the
musician plays the third minor chord.

The other musician is doing something a little weird, playing power chords all along the scale, but 3 octaves down.

As the API evolves, musicians will be able to listen more to one another, and there will be all sorts of new ways to introduce
routing interestingness, randomness, and evolution.

Architecture
============

Things are still evolving a lot.  Read the code for now.  Notes pending!

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

Setup
=====

It's recommended you target some soft synths running inside a Digital Audio Workstation program (DAW) or standalone.  

Initial testing in the early days of this program were done against Native Instrument's Absynth.

For OS X:

    brew install python3
    pip3 install -r requirements.txt

Open "Audio/MIDI Setup" on OS X, pick "Window / Open MIDI  Studio" and click on the IAC Driver Block.  Pick "Enabled" and make sure
there are some MIDI ports there.

Then:
 
   make tests

If you skip the IAC step the tests may fail. 

If you have problems with this step (or want to share Windows/Linux tips), stop by the mailing list!

Author
======

   * CAMP is written by Michael DeHaan (michael.dehaan@gmail.com)

