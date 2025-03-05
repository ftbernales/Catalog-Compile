import os
import toml
from catcompile.utils import sap


def main(dirname):
    """
    Convert all .yml files in the given directory into .toml files,
    recursively.
    """
    import yaml
    for cwd, dir_, fnames in os.walk(dirname):
        for fname in fnames:
            if fname.endswith('.yml'):
                path = os.path.join(cwd, fname)
                with open(path) as source:
                    dic = yaml.safe_load(source.read())
                with open(path[:-3] + 'toml', 'w') as target:
                    toml.dump(dic, target)
                print('Saved %s' % target.name)


main.dirname = 'directory'


if __name__ == '__main__':
    sap.run(main)