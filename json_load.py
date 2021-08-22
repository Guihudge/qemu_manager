import json
import qemu_base_tools
import qemu_arm_tools
import qemu_x86_tools
import qemu_disk_tools

import constant

"""
vm_save_format:
arch : str
cpu : int
ram : str
kvm : bool
cpu/machine : str
iso : list
disk: list(dict[disk_format}])


disk_format:
file: str
interface: str
type: str
format: str
"""


def load_json(file):
    f = open(file, "r")
    x = json.load(f)
    return x


def base_cmd(dico):
    cmd = qemu_base_tools.make_base_cmd(
        constant.qemu_base, dico["arch"], constant.qemu_allocate_ram, dico["ram"], constant.qemu_allocate_cpu_core, str(dico["core"]))

    if dico["arch"] == "x86_64" or "i386":
        cmd = qemu_x86_tools.add_cpu_to_cmd(cmd, dico["cpu"])
    else:
        cmd = qemu_arm_tools.add_platform_to_cmd(cmd, dico["cpu"])

    if dico["kvm"]:
        cmd = cmd + " -enable-kvm"

    return cmd


def load_iso(cmd, dico):
    for iso in dico["iso"]:
        cmd = cmd + " -cdrom " + iso
    return cmd


def load_disk(cmd, dico):
    for disk in dico["disk"]:
        cmd += qemu_disk_tools.create_disk_drive_vm(
            disk["file"], disk["interface"], disk["type"], disk["format"])
    return cmd


def gen_cmd_from_save(file):
    save = load_json(file)
    cmd = base_cmd(save)
    cmd = load_iso(cmd, save)
    cmd = load_disk(cmd, save)

    return cmd
