import os
import sys
default_stdout = sys.stdout
def clean():
    sys.stdout = default_stdout
try:
    while True:
        clean()
        print(
        """
        QEMU启动器 version Alpha
        ----------------------------------------------------------------------------------------
        [1]安装QEMU(不兼容Windows)
        [2]创建虚拟机
        [3]运行虚拟机
        [4]删除虚拟机
        [5]退出
        ----------------------------------------------------------------------------------------
        """
        )
        opt = input()
        if opt == '1':
            clean()
            pkg = input('请输入软件包管理器名称：')
            os.system('sudo ' + pkg + ' install qemu')
        elif opt == '2':
            clean()
            name = input('请输入虚拟机名称:')
            disk = input('请输入虚拟磁盘大小(GB)：')
            cd = input('请输入光盘路径：')
            memory = input('请输入内存大小(MB)：')
            os.system('qemu-img create -f qcow2 ' + name + '.qcow2 ' + disk + 'G')
            with open('VM配置文件/vms', 'w+') as i:
                try:
                    _i = eval(i.read())
                except SyntaxError:
                    _i = []
                _i.append(name)
                i.write(str(_i))
            with open('VM配置文件/' + name, 'w+') as i:
                i.write(str([cd, memory]))
            os.system('qemu-system-x86_64 -hda ' + name + '.qcow2 -cdrom ' + cd + ' -m ' + memory + 'M --enable-kvm')
        elif opt == '3':
            clean()
            with open('VM配置文件/vms', 'r') as i:
                vmlist = eval(i.read())
            print('虚拟机列表：')
            _ = 0
            for i in vmlist:
                print(_, '|', i)
                _ += 1
            no_ = int(input('请输入编号：'))
            with open('VM配置文件/' + vmlist[no_]) as i:
                i_ = eval(i.read())
                name = vmlist[no_]
                cd = i_[0]
                memory = i_[1]
            os.system('qemu-system-x86_64 -hda ' + name + '.qcow2 -cdrom ' + cd + ' -m ' + memory + 'M')

        elif opt == '4':
            clean()
            with open('VM配置文件/vms', 'r') as i:
                try:
                    vmlist = eval(i.read())
                except SyntaxError:
                    vmlist = []
            print('虚拟机列表：')
            _ = 0
            for i in vmlist:
                print(_, '|', i)
                _ += 1
            no_ = int(input('请输入编号：'))
            clean()
            with open('VM配置文件/vms', 'r') as i:
                vmlist = eval(i.read())
            os.remove('VM配置文件/' + vmlist[no_])
            os.remove(vmlist[no_] + '.qcow2')
            with open('VM配置文件/vms', 'w+') as i:
                
                _i = eval(i.read())

                _i.remove(vmlist[no_])
                i.write(str(_i))
            print('删除成功！')
        elif opt == '5':
            exit()
        else:
            print('没有这个选项！（按Enter继续）')
            input()
except Exception as e:
    clean()
    print('发生错误，错误代码：', e)
    input('按Enter继续')
    exit()        
                    
