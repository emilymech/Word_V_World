from pathlib import Path

body_path = Path('/Volumes/research_data') / 'Word_V_World' / 'runs' / 'Wiki_Heads_Bodies' / 'bodies.txt'
output_path = Path('/Volumes/research_data') / 'Word_V_World' / 'runs' / 'Wiki_Heads_Bodies' / 'small_bodies'

# TODO this will need to be rewritten, because there will be 7 bodies.txt files, each belonging to the same corpus

lines_per_file = 5655
smallfile = None
with open(body_path) as bigfile:
    print("Let the bodies hit the floor...")
    for lineno, line in enumerate(bigfile):

        # open new file at some interval - very clever
        if lineno % lines_per_file == 0:
            if smallfile:
                smallfile.close()
            small_filename = output_path / 'body_{}.txt'.format(lineno + lines_per_file)
            smallfile = open(small_filename, "w")

        # write line to file
        smallfile.write(line)

    # close last file
    if smallfile:
        smallfile.close()

