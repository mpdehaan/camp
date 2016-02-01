from camp.core.note import Note

class TestNote(object):

   def test_comparisons(self):

       assert Note(name='C', octave=4) > Note(name='C', octave=3)
       # FIXME: more tests for note differences
       # FIXME: more tests for octaves

   def test_transpose(self):

       assert Note(name='C', octave=4).transpose(steps=0.5) == Note(name='Db', octave=4)
       # FIXME: more tests for positive half steps
       # FIXME: more tests for positive whole steps
       # FIXME: tests for positive octaves 
       # FIXME: tests for negatives

   def test_equivalence(self):
       assert Note(name='Db', octave=4) == Note(name='C#', octave=4)
       # FIXME: more tests


