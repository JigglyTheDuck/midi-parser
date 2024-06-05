# Jiggly midi parser

Use this utility to turn a midi file into Jiggly-compatible sound commands.

The parser is rather rudimentary but it usually gets the job done, still if you put your mind to it, you can easily improve on it.

## Install

It's a simple python script, so it's ready to go right after you pull the repo and install the requirements.
```
pip install -r requirements.txt
```

## Usage

to use the parser simply add the input file as the last argument
```
python ./parser.py the-song.mid
```

It will output the Jiggly compatible sound commands to the standard output.

*Hint: if you're on a mac, you can use `| pbcopy` to pipe the output to the clipboard directly. Other options are available for other systems.*

The parser has 2 modes of operation depending on the input midi file:

- Single channel: If the midi file does not specify a channel but uses the `flat` measures the parser can be used by simply specifying the midi file name without issues.

- Multi-channel Usually, midi files define multiple instrument channels but Jiggly only has 3 (and it is further limited to playing a single note at once). Therefore to be able to play multiple notes at a time, the parser is equipped with a channel synchronizer that uses all 3 sound channels to sample a single midi channel. To select the specific channel simply specify the `-c` argument like this:
```
python ./parser.py -c 2 the-song.mid
```

This will take only the 2nd channel of the midi file.
