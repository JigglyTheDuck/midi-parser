from music21 import converter, instrument, note, chord, pitch
import argparse

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

def get_notes_from_measure(measure):
    """ Retrieve all notes and chords from a measure. """
    notes = []
    for element in measure.notes:
        if isinstance(element, note.Note):
            notes.append(str(element.nameWithOctave))
        elif isinstance(element, chord.Chord):
            notes.append('.'.join(str(n) for n in element.normalOrder))
    return notes

def parse_quarter_length(quarter_length):
    if quarter_length == 0.25: return 1
    if quarter_length == 0.5: return 2
    if quarter_length == 0.75: return 3
    if quarter_length == 1: return 4
    if quarter_length == 1.25: return 5
    if quarter_length == 1.5: return 6
    if quarter_length == 1.75: return 7
    if quarter_length == 2: return 8
    if quarter_length == 2.5: return 9
    if quarter_length == 2.75: return 10
    if quarter_length == 3: return 12
    if quarter_length == 3.5: return 14
    if quarter_length == 4: return 16

    if abs(quarter_length - 1 / 6) < 0.1: return 1
    if abs(quarter_length - 2 / 3) < 0.1: return 3
    if abs(quarter_length - 4 / 3) < 0.1: return 5
    if abs(quarter_length - 5 / 12) < 0.1: return 2

    raise TypeError(f'unsupported quarter length: {quarter_length}')



class Channel():
    def __init__(self):
        self.octave = 3
        self.seek = 0
        self.commands = []

    def sync_to(self, seek):
        while self.seek < seek:
            rest = 16 if seek - self.seek > 16 else seek - self.seek
            self.commands.append(f'  rest {rest}')
            self.seek += rest

    def change_octave(self, octave):
        if self.octave != octave:
            self.commands.append(f'  octave {octave}')
            self.octave = octave

    def note(self, note, quarterLength):
        l = parse_quarter_length(quarterLength)
        note_name = note.name if len(note.name) > 1 else f'{note.name}_'

        p = pitch.Pitch(note.name)

        if p.accidental and p.accidental.name == 'flat':
            note_name = p.getEnharmonic()

        self.change_octave(note.octave);

        self.commands.append(f'  note {note_name} {l}')

        self.seek += l;

        return l

    def __str__(self):
        str = 'channel::\n'
        str += '.loop:\n'
        str += '\n'.join(self.commands)
        str += '\nsound_loop 0, .loop'
        return str

def parse_measure(channels, measure):
    for element in measure.notes:
        if channels[0].seek > 1000: return
        if isinstance(element, note.Rest):
            print("REST - not implemented");
        if isinstance(element, note.Note):
            channels[0].note(element, element.quarterLength);
        elif isinstance(element, chord.Chord):
            for i, n in enumerate(element.notes):
                if i > 2: break
                if i > 0:
                    channels[i].sync_to(channels[0].seek);
                channels[i].note(n, element.quarterLength)

def parse_midi(file_path, channel):
    channels = [Channel(), Channel(), Channel()]
    # Load the MIDI file
    midi = converter.parse(file_path)

    if channel is None: parse_measure(channels, midi.flat);
    for i, part in enumerate(midi.parts):
        if channel is not None and channel != i: continue
        for measure in part.getElementsByClass('Measure'):
            parse_measure(channels, measure)

    for channel in channels:
        channels[1].sync_to(channels[0].seek);
        channels[2].sync_to(channels[0].seek);
        

    return channels

def main():
    parser = argparse.ArgumentParser(description="A simple script to demonstrate argparse.")
    parser.add_argument('filename', type=str, help='The name of the file to process')
    parser.add_argument('--channel', '-c', type=check_positive, help='midi channel (part) to parse')

    args = parser.parse_args()

    channels = parse_midi(args.filename, args.channel)

    for channel in channels:
        print(channel)

if __name__ == '__main__':
    main()
