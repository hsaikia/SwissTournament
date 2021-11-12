import fire

from swiss_tournament.commands import Commands

if __name__ == '__main__':
    commands = Commands()
    fire.Fire(commands)
