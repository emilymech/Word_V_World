import importlib
import sys

from word_v_world import config

for param_p, label in client.gen_param_ps(PARAM2REQUESTS):
    bodies_path = list(param_p.glob('**/bodies.txt'))[0]

    # measure size of bodies.txt file in MBs
    num_bytes = bodies_path.stat().st_size
    num_megabytes = num_bytes >> 20
    print('{} contains {} MBs'.format(bodies_path.relative_to(config.RemoteDirs.research_data), num_megabytes))
    print()


