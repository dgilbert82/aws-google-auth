#!/usr/bin/env python

import getpass
import os
from collections import OrderedDict
from tabulate import tabulate
from . import renderoutput


class Util:

    @staticmethod
    def show_output(use_gui, message):
        surface = 'console'
        if use_gui:
            surface = 'gui'
        renderSurface = renderoutput.Surface(surface)
        return renderSurface.displayMessage(message)


    @staticmethod
    def get_input(use_gui, prompt):
        surface = 'console'
        if use_gui:
            surface = 'gui'
        renderSurface = renderoutput.Surface(surface)
        return renderSurface.getInput(prompt)
        

    @staticmethod
    def get_pass(use_gui, prompt):
        surface = 'console'
        if use_gui:
            surface = 'gui'
        renderSurface = renderoutput.Surface(surface)
        return renderSurface.getPass(prompt)

    @staticmethod
    def pick_a_role(use_gui, roles, aliases=None):
        if aliases:
            enriched_roles = {}
            for role, principal in roles.items():
                enriched_roles[role] = [
                    aliases[role.split(':')[4]],
                    role.split('role/')[1],
                    principal
                ]
            enriched_roles = OrderedDict(sorted(enriched_roles.items(), key=lambda t: (t[1][0], t[1][1])))

            ordered_roles = OrderedDict()
            for role, role_property in enriched_roles.items():
                ordered_roles[role] = role_property[2]

            enriched_roles_tab = []
            for i, (role, role_property) in enumerate(enriched_roles.items()):
                enriched_roles_tab.append([i + 1, role_property[0], role_property[1]])

            while True:
                self.show_output(tabulate(enriched_roles_tab, headers=['No', 'AWS account', 'Role'], ))
                prompt = 'Type the number (1 - {:d}) of the role to assume: '.format(len(enriched_roles))
                choice = Util.get_input(use_gui, prompt)

                try:
                    return list(ordered_roles.items())[int(choice) - 1]
                except IndexError:
                    Util.show_output(use_gui, "Invalid choice, try again.")
        else:
            role_list = ''
            while True:
                for i, role in enumerate(roles):
                    role_list += "[{:>3d}] {}\n".format(i + 1, role)

                Util.show_output(use_gui, role_list)
                prompt = 'Type the number (1 - {:d}) of the role to assume: '.format(len(roles))
                choice = Util.get_input(use_gui, prompt)

                try:
                    return list(roles.items())[int(choice) - 1]
                except IndexError:
                    Util.show_output(use_gui, "Invalid choice, try again.")

    @staticmethod
    def touch(file_name, mode=0o600):
        flags = os.O_CREAT | os.O_APPEND
        with os.fdopen(os.open(file_name, flags, mode)) as f:
            try:
                os.utime(file_name, None)
            finally:
                f.close()

    # This method returns the first non-None value in args. If all values are
    # None, None will be returned. If there are no arguments, None will be
    # returned.
    @staticmethod
    def coalesce(*args):
        for number, value in enumerate(args):
            if value is not None:
                return value
        return None

    @staticmethod
    def unicode_to_string_if_needed(object):
        if "unicode" in str(object.__class__):
            return object.encode('utf-8')
        else:
            return object
