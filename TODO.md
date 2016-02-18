TODO List
=========

High priority:
 * Hook Control-C to avoid stuck notes (conductor.py)

Medium:
 * More examples (examples folder)
 * Make a Pattern Router that allows for choosing one of many patterns to fire, kind of the opposite of Ordered, which runs one, then the other.
 * Cleanup README
 * Start thinking about ways to express these configurations in non-code (YAML tracker?) - should be mostly fully featured (arps, etc!) and allow for routing maps.
 * Add a source similar to velocity and duration but for MIDI CC control change - filter sweeps, etc.
 * Add a delay source, should be possible to delay note start, stop, or both.

Low:
 * Remove old comments
 * A selector that takes an arbitrary callback, which could be used to implement sine waves and other crazy things not in the core
 * Think about coordination between nodes.
 * Right now the base beat is a quarter note, how to make it cleaner to configure to avoid thinking about subdivide often
 * Think about nodes that have a buffer and "spy" on events from other nodes - to implement more "jazz" like ideas 
 * Better code sharing between subdivide.py and arp.py
 * More features for selector Randomly, as noted in examples/ file
 * Architecture writeup / intro docs
 * Understand if the return codes of member.signal are meaningful.
 * Think about better syntactic sugar for connecting nodes together
 * Go through all the member.*/selector.* code and make it more elegant using clever syntactic sugar and useful helper methods.
