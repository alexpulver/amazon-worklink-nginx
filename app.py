import json
import os
import sys

from aws_cdk import core

from nginx import Nginx


def main():
    config_file_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_file_path) as config_file:
        config = json.load(config_file)
    env = {
        'account': config['account'],
        'region': config['region']
    }

    app = core.App()
    Nginx(app, 'nginx', config=config, env=env)
    app.synth()


if __name__ == '__main__':
    sys.exit(main())
