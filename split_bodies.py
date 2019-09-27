from pathlib import Path

body_path = Path('/Volumes/research_data') / 'Word_V_World' / 'runs' / 'Wiki_Heads_Bodies' / 'bodies.txt'
output_path = Path('/Volumes/research_data') / 'Word_V_World' / 'runs' / 'Wiki_Heads_Bodies' / 'small_bodies'

lines_per_file = 5655
smallfile = None
with open(body_path) as bigfile:
    print("Let the bodies hit the floor...")
    for lineno, line in enumerate(bigfile):
        if lineno % lines_per_file == 0:
            if smallfile:
                smallfile.close()
            small_filename = output_path / 'body_{}.txt'.format(lineno + lines_per_file)
            smallfile = open(small_filename, "w")
        smallfile.write(line)
    if smallfile:
        smallfile.close()

