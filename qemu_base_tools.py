import os
import subprocess
import shutil


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


def get_nproc():
    cmd = ["nproc"]
    output = subprocess.run(cmd, stdout=subprocess.PIPE)
    all_cmd = str(output.stdout.decode("utf-8"))
    return int(all_cmd)


def get_total_host_mem():
    cmd = ["grep", "MemTotal", "/proc/meminfo"]
    output = subprocess.run(cmd, stdout=subprocess.PIPE)
    all_cmd = str(output.stdout.decode("utf-8"))
    mem_kB = int(all_cmd.split(" ")[7])
    mem_MB = int(mem_kB / 1024)
    return mem_MB


def get_free_disk_space_GB(path):
    total, used, free = shutil.disk_usage(path)
    space_o = int(free)
    space_ko = int(space_o / 1024)
    space_Mo = int(space_ko / 1024)
    space_Go = space_Mo / 1024
    return space_Go


get_free_disk_space_GB("/home/guillaume")
