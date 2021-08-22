import tools_kit

import glob
import constant
import subprocess


def add_iso_to_cmd(path, cmd):
    return cmd + " -cdrom " + path


def list_file(path):
    file_list = glob.glob(path)
    return file_list


def create_disk(name, format, size):
    cmd = ["qemu-img", "create", "-f", format, name, size]
    output = subprocess.run(cmd, stdout=subprocess.PIPE)
    print(str(output.stdout.decode("utf-8")))
    print("disk created!")


def info_disk(name):
    cmd = ["qemu-img", "info", name]
    output = subprocess.run(cmd, stdout=subprocess.PIPE)
    print(str(output.stdout.decode("utf-8")))


def resize_disk(name, new_size):
    cmd = ["qemu-img", "resize", name, new_size]
    output = subprocess.run(cmd, stdout=subprocess.PIPE)
    print(str(output.stdout.decode("utf-8")))


def create_disk_drive_vm(file, interface, type, format):
    drive_cmd = ' -drive "file={},if={},media={},format={}"'.format(
        file, interface, type, format)
    return drive_cmd


def iso_setup(cmd):
    if tools_kit.check_yn("Use iso file? [y/n] : "):
        iso = tools_kit.choose_list(list_file(
            constant.default_iso_path), "Choose iso: ")
        cmd = add_iso_to_cmd(iso, cmd)
    return cmd


def disk_setup(cmd):
    if tools_kit.check_yn("Use disk file? [y/n] : "):
        print("1: create disk\n2: use existant disk")
        rep = int(input("Choose: "))

        if rep == 1:
            name = input("disk name (without extension): ")
            format = tools_kit.choose_list(
                ["qcow2", "raw"], "choose format of disk: ")
            name = constant.default_disk_path + name + "." + format
            size = input("disk size with prefix (M for Mo, G for Go): ")
            create_disk(name, format, size)

            print("\n\n setup drive:")
            interface = tools_kit.choose_list(
                ["virtio", "ide", "scsi", "sata"], "Choose interface for disk: ")
            type = "disk"
            drive = create_disk_drive_vm(name, interface, type, format)

            cmd = cmd + drive

        if rep == 2:
            file = tools_kit.choose_list(
                list_file(constant.default_disk_path+"*"), "Choose disk: ")
            interface = tools_kit.choose_list(
                ["virtio", "ide", "scsi", "sata"], "Choose interface for disk: ")
            format = tools_kit.choose_list(
                ["qcow2", "raw"], "choose format of disk: ")
            type = "disk"

            drive = create_disk_drive_vm(file, interface, type, format)

            cmd = cmd + drive
    return cmd
