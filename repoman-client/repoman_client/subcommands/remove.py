from repoman_client.subcommand import SubCommand
from repoman_client.client import RepomanClient, RepomanError
from repoman_client.config import config
from argparse import ArgumentParser
import sys

def yes_or_no():
    answer = raw_input("Confirm deletion [yes]/[n]o: ")
    attempts = 1
    while answer in ['y', 'ye']:
        if attempts >= 3:
            break
        answer = raw_input("Type the full word 'yes' to confirm deletion: ")
        attempts = attempts + 1

    if answer.lower() in ['yes']:
        return True
    else:
        return False



class RemoveUser(SubCommand):
    command_group = "advanced"
    command = "remove-user"
    alias = None
    description = 'Remove an existing user from the repository'

    def get_parser(self):
        p = ArgumentParser(self.description)
        p.add_argument('user', help='The user you wish to remove')
        p.add_argument('-f', '--force', action='store_true', default=False,
                       help='Do not ask for conformation before deleting')
        return p

    def __call__(self, args, extra_args=None):
        repo = RepomanClient(config.host, config.port, config.proxy)
        if not args.force:
            print ("WARNING:\n"
                    "\tAll images owned by the user will be removed.\n"
                    "\tThis operation cannot be undone!")
            if not yes_or_no():
                print "Aborting user deletion"
                return
        try:
            repo.remove_user(args.user)
        except RepomanError, e:
            print e
            sys.exit(1)




class RemoveGroup(SubCommand):
    command_group = "advanced"
    command = "remove-group"
    alias = None
    description = 'Remove an existing group from the repository'

    def get_parser(self):
        p = ArgumentParser(self.description)
        p.add_argument('group', help='The group you wish to remove')
        p.add_argument('-f', '--force', action='store_true', default=False,
                       help='Do not ask for conformation before deleting')
        return p

    def __call__(self, args, extra_args=None):
        repo = RepomanClient(config.host, config.port, config.proxy)
        if not args.force:
            if not yes_or_no():
                print "Aborting group deletion"
                return

        try:
            repo.remove_group(args.group)
        except RepomanError, e:
            print e
            sys.exit(1)


class RemoveImage(SubCommand):
    command_group = "advanced"
    command = 'remove-image'
    alias = None
    description = 'Delete an image from the repository'

    def get_parser(self):
        p = ArgumentParser(self.description)
        p.add_argument('image', metavar='[USER/]IMAGE',
                       help='name of image to delete')
        p.add_argument('-f', '--force', action='store_true', default=False,
                       help='Delete image without prompting')
        return p

    def __call__(self, args, extra_args=None):
        repo = RepomanClient(config.host, config.port, config.proxy)
        if not args.force:
            print ("WARNING:\n"
                    "\tdeleting an image cannot be undone.\n")
            if not yes_or_no():
                print "Aborting user deletion"
                return

        try:
            repo.remove_image(args.image)
        except RepomanError, e:
            print e
            sys.exit(1)



class Delete(RemoveImage):
    # subclass RemoveImage because they are the same command.
    command_group = None
    command = "delete"
    alias = None

