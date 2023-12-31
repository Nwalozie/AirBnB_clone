#!/usr/bin/python3
"""Importing the necessary classes and modules"""

import cmd
import sys
from models.base_model import BaseModel
from models import storage
from models import storage
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Class that creates the console module"""

    instances = {}
    prompt = "(hbnb) "

    def do_EOF(self, line):
        """Handling End Of file
        """
        return True

    def do_quit(self, line):
        """Handling Quit command
        """
        return True

    def emptyline(self):
        """Handling empty lines
        """
        pass

    def do_create(self, line):
        """Handling the create command
        """
        if not line:
            print("** class name missing **")
            return
        class_name = line.split()[0]
        try:
            model_class = globals()[class_name]
            print(model_class)
            new_instance = model_class()
            new_instance.save()
            print(new_instance.id)
        except KeyError:
            print("** class doesn't exist **")

    def do_show(self, line):
        """Handling the show command
        """
        if not line:
            print("** class name missing **")
        else:
            args = line.split()

            class_name = args[0] if len(args) >= 1 else None
            instance_id = args[1] if len(args) > 1 else None

            try:
                model_ = globals()[class_name]
            except KeyError:
                print("** class doesn't exist **")
            else:
                if instance_id is None:
                    print("** instance id missing **")
                    return

                dic = storage.all()
                key = "{}.{}".format(class_name, instance_id)
                if key in dic:
                    print(dic[key])
                else:
                    print("** no instance found **")

    def do_destroy(self, line):
        """Handling the destroy command
        """
        if not line:
            print("** class name missing **")
        else:
            args = line.split()

            class_name = args[0] if len(args) >= 1 else None
            instance_id = args[1] if len(args) > 1 else None

            try:
                model_ = globals()[class_name]
            except KeyError:
                print("** class doesn't exist **")
            else:
                if instance_id is None:
                    print("** instance id missing **")
                    return

                dic = storage.all()
                key = "{}.{}".format(class_name, instance_id)
                if key in dic:
                    del dic[key]
                    storage.save()
                else:
                    print("** no instance found **")

    def do_all(self, arg):
        """Handling the all command
        """
        class_name = arg.split()[0] if arg else None
        if class_name and class_name not in storage.all_classes():
            print("** class doesn't exist **")
            return

        all_instances = storage.all()
        if class_name:
            instances = [str(instance) for instance in all_instances.values()
                         if
                         instance.__class__.__name__ == class_name]
        else:
            instances = [str(instance) for instance in all_instances.values()]

        print(instances)

    def do_update(self, line):
        """Handling the Update command"""
        args = line.split()

        if not args:
            print("** class name missing **")
            return
        class_name = args[0]

        if class_name not in storage.all_classes():
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        if "{}.{}".format(class_name, instance_id) not in storage.all():
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        attribute_name = args[2]
        value = args[3]

        instance = storage.all()["{}.{}".format(class_name, instance_id)]
        try:
            value = type(getattr(instance, attribute_name))(value)
        except (ValueError, AttributeError):
            pass
        setattr(instance, attribute_name, value)
        instance.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
