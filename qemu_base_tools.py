import os
import subprocess


def launch(cmd):
    os.system(cmd)


def make_base_cmd(base, arch, ram, ram_qty, core, core_qty):
    cmd = base + arch + " " + ram + " " + \
        ram_qty + " " + core + " " + core_qty
    return cmd


def list_arch(qemu_path):
    cmd = ["ls", qemu_path]
    output = subprocess.run(cmd, stdout=subprocess.PIPE)
    all_cmd = str(output.stdout.decode("utf-8"))
    list_cmd = all_cmd.split("\n")
    qemu_list = []
    for i in list_cmd:
        base = i[0:11]
        if base == "qemu-system":
            qemu_list.append(i)

    arch_list = []
    for arch in qemu_list:
        type = arch.split("-", 2)
        arch_list.append(type[2])

    return arch_list


def kvm_enable(cmd, host_arch, dest_arch):
    if host_arch == dest_arch + "\n":
        rep = input("Enable kvm? [y/n] : ")
        if rep == "y" or rep == "Y":
            cmd = cmd + " -enable-kvm"
            return cmd
    else:
        print("kvm not available for the choosen arch. sorry ;(")
    return cmd


def get_base_params(params: str):
    params_list = params.split(" ", 1)
    return params_list[0]


def get_host_type():
    cmd = ["uname", "-m"]
    output = subprocess.run(cmd, stdout=subprocess.PIPE)
    all_cmd = str(output.stdout.decode("utf-8"))
    return all_cmd
