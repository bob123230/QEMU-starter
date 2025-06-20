import os
import sys


# 清屏函数，根据操作系统选择命令
def clean():
    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")

try:
    while True:
        clean()
        print(
        """
        QEMU启动器 version 0.3
        ----------------------------------------------------------------------------------------
        [1]安装QEMU
        [2]创建虚拟机
        [3]运行虚拟机
        [4]删除虚拟机
        [5]修改虚拟机参数
        [6]退出
        ----------------------------------------------------------------------------------------
        """
        )
        while True:
            opt = input()  # 获取用户输入的选项
            if opt not in ['1', '2', '3', '4', '5', '6']:
                print('没有这个选项！（请输入1-6）')
                continue
            break
        if opt == '1':
            clean()
            # 安装QEMU
            if sys.platform == "win32": # Windows下自动下载QEMU安装包
                print("正在下载QEMU Windows安装包...")
                try:
                    import requests
                except ImportError:
                    print("未检测到requests库，正在尝试安装...")
                    os.system("pip install requests")
                    import requests
                url = "https://qemu.weilnetz.de/w64/qemu-w64-setup-20250422.exe"
                local_filename = "qemu-w64-setup-20250422.exe"
                try:
                    # 下载QEMU安装包
                    with requests.get(url, stream=True) as r:
                        r.raise_for_status()
                        with open(local_filename, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                    print(f"下载完成，正在启动安装包安装。。。")
                    os.system(local_filename)
                except Exception as e:
                    print(f"下载失败: {e}")
            else:
                # Linux/macOS下通过包管理器安装
                while True:
                    pkg = input('请输入软件包管理器名称：')
                    if pkg.strip() == "":
                        print("软件包管理器名称不能为空，请重新输入。")
                    else:
                        break
                os.system('sudo ' + pkg + ' install qemu')
        elif opt == '2':
            clean()
            # 创建虚拟机
            while True:
                name = input('请输入虚拟机名称:')
                if name.strip() == "":
                    print("虚拟机名称不能为空，请重新输入。")
                else:
                    break
            while True:
                disk = input('请输入虚拟磁盘大小(GB)：')
                try:
                    disk_val = int(disk)
                    if disk_val <= 0:
                        print("磁盘大小必须为正整数，请重新输入。")
                        continue
                    break
                except ValueError:
                    print("请输入有效的数字。")
            while True:
                cd = input('请输入光盘路径：')
                if cd.strip() == "":
                    print("光盘路径不能为空，请重新输入。")
                else:
                    break
            while True:
                memory = input('请输入内存大小(MB)：')
                try:
                    memory_val = int(memory)
                    if memory_val <= 0:
                        print("内存大小必须为正整数，请重新输入。")
                        continue
                    break
                except ValueError:
                    print("请输入有效的数字。")
            while True:
                cpu = input('请输入架构：')
                if cpu.strip() == "":
                    print("架构不能为空，请重新输入。")
                else:
                    break
            while True:
                kvm = input('是否启用KVM？(y/n)：').lower()
                if kvm not in ['y', 'n']:
                    print("请输入y或n。")
                else:
                    break
            
            # 创建虚拟磁盘
            os.system('qemu-img create -f qcow2 ' + name + '.qcow2 ' + disk + 'G')
            # 记录虚拟机名称到vms文件
            with open('VM配置文件/vms', 'w+') as i:
                try:
                    _i = eval(i.read())
                except SyntaxError:
                    _i = []
                _i.append(name)
                i.write(str(_i))
            # 保存虚拟机配置
            with open('VM配置文件/' + name, 'w+') as i:
                if kvm == 'y':
                    i.write(str([cd, memory, cpu, True]))
                else:
                    i.write(str([cd, memory, cpu, False]))
            # 启动虚拟机
            if kvm == 'y':
                os.system('qemu-system-' + cpu + ' -hda ' + name + '.qcow2 -cdrom ' + cd + ' -m ' + memory + 'M --enable-kvm')
            else:
                os.system('qemu-system-' + cpu + ' -hda ' + name + '.qcow2 -cdrom ' + cd + ' -m ' + memory + 'M')
        elif opt == '3':
            clean()
            # 运行虚拟机
            with open('VM配置文件/vms', 'r') as i:
                vmlist = eval(i.read())
            if not vmlist:
                print("没有可用虚拟机。按Enter返回。")
                input()
                continue
            print('虚拟机列表：')
            _ = 0
            for i in vmlist:
                print(_, '|', i)
                _ += 1
            while True:
                no_ = input('请输入编号：')
                try:
                    no_ = int(no_)
                    if 0 <= no_ < len(vmlist):
                        break
                    else:
                        print("编号超出范围，请重新输入。")
                except ValueError:
                    print("请输入有效的数字编号。")
            with open('VM配置文件/' + vmlist[no_]) as i:
                i_ = eval(i.read())
                name = vmlist[no_]
                cd = i_[0]
                memory = i_[1]
                cpu = i_[2]
                kvm = i_[3]
                # 根据KVM选项启动虚拟机
                if kvm:
                    os.system('qemu-system-' + cpu + ' -hda ' + name + '.qcow2 -cdrom ' + cd + ' -m ' + memory + 'M --enable-kvm')
                else:
                    os.system('qemu-system-' + cpu + ' -hda ' + name + '.qcow2 -cdrom ' + cd + ' -m ' + memory + 'M')
        elif opt == '4':
            clean()
            # 删除虚拟机
            with open('VM配置文件/vms', 'r') as i:
                try:
                    vmlist = eval(i.read())
                except SyntaxError:
                    vmlist = []
            if not vmlist:
                print("没有可用虚拟机。按Enter返回。")
                input()
                continue
            print('虚拟机列表：')
            _ = 0
            for i in vmlist:
                print(_, '|', i)
                _ += 1
            while True:
                no_ = input('请输入编号：')
                try:
                    no_ = int(no_)
                    if 0 <= no_ < len(vmlist):
                        break
                    else:
                        print("编号超出范围，请重新输入。")
                except ValueError:
                    print("请输入有效的数字编号。")
            clean()
            with open('VM配置文件/vms', 'r') as i:
                vmlist = eval(i.read())
            # 删除配置文件和磁盘文件
            os.remove('VM配置文件/' + vmlist[no_])
            os.remove(vmlist[no_] + '.qcow2')
            # 更新vms文件
            with open('VM配置文件/vms', 'r+') as i:
                try:
                    _i = eval(i.read())
                except SyntaxError:
                    _i = []
                _i.remove(vmlist[no_])
                i.write(str(_i))
            print('删除成功！')
        elif opt == '5':
            clean()
            # 修改虚拟机参数
            with open('VM配置文件/vms', 'r') as i:
                vmlist = eval(i.read())
            if not vmlist:
                print("没有可用虚拟机。按Enter返回。")
                input()
                continue
            print('虚拟机列表：')
            _ = 0
            for i in vmlist:
                print(_, '|', i)
                _ += 1
            while True:
                no_ = input('请输入编号：')
                try:
                    no_ = int(no_)
                    if 0 <= no_ < len(vmlist):
                        break
                    else:
                        print("编号超出范围，请重新输入。")
                except ValueError:
                    print("请输入有效的数字编号。")
            while True:
                disk = input('请输入虚拟磁盘大小(GB)：')
                try:
                    disk_val = int(disk)
                    if disk_val <= 0:
                        print("磁盘大小必须为正整数，请重新输入。")
                        continue
                    break
                except ValueError:
                    print("请输入有效的数字。")
            while True:
                cd = input('请输入光盘路径：')
                if cd.strip() == "":
                    print("光盘路径不能为空，请重新输入。")
                else:
                    break
            while True:
                memory = input('请输入内存大小(MB)：')
                try:
                    memory_val = int(memory)
                    if memory_val <= 0:
                        print("内存大小必须为正整数，请重新输入。")
                        continue
                    break
                except ValueError:
                    print("请输入有效的数字。")
            while True:
                cpu = input('请输入架构：')
                if cpu.strip() == "":
                    print("架构不能为空，请重新输入。")
                else:
                    break
            while True:
                kvm = input('是否启用KVM？(y/n)：').lower()
                if kvm not in ['y', 'n']:
                    print("请输入y或n。")
                else:
                    break
            # 保存新的配置
            with open('VM配置文件/' + vmlist[no_], 'w+') as i:
                if kvm == 'y':
                    i.write(str([cd, memory, cpu, True]))
                else:
                    i.write(str([cd, memory, cpu, False]))
            print('修改成功！')
        elif opt == '6':
            exit()    # 退出程序

except Exception as e:
    clean()
    print('发生错误，错误代码：', e)
    if input('按Enter继续') == 'stderr':
        raise
    exit()

