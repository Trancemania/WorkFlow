import sys
import os
import subprocess as sub
import time
import re
import pyautogui
from pynput.keyboard import _darwin #不能删，否则打包后有问题
from pynput.mouse import _darwin    #不能删，否则打包后有问题
from pynput.mouse import Controller,Button


class WorkFlow:
    def __init__(self):
        pass

    def get_all_process(self):
        """获取所有正在运行的进程名"""
        script = '''
        tell application "System Events"
            set listOfProcesses to every process
            set allProcess to {} 
            repeat with processItem in listOfProcesses
                set procname to name of processItem as string
                set processId to unix id of processItem as string
                set processDic to {procname}
                copy processDic to end of allProcess
            end repeat
            return allProcess
        end tell
        '''
        p = sub.Popen(['osascript', '-e',script], stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
        stdout, stderr = p.communicate()
        if 'error' in stderr:
            raise Exception(stderr)
        process_list = [pr.strip() for pr in stdout.split(',')]
        process_list.sort()
        return process_list

    def get_all_windows(self):
        """
        获取所有窗口
        返回[app名称,窗口名称]的列表，如
        ['Finder_Recents', 'pycharm_MacOS – WorkFlow.py', 'Terminal_wheels — -bash — 80×24', 'System Preferences_Sharing']
        """
        script = '''
        tell application "System Events"
            set this_info to {}
            repeat with theProcess in (application processes where visible is true)
                try
                set this_info to this_info & (value of (first attribute whose name is "AXWindows") of theProcess)
                end try
            end repeat
            this_info -- display list in results window of AppleScript Editor 
        end tell
        '''
        p = sub.Popen(['osascript', '-e',script], stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
        stdout, stderr = p.communicate()
        if 'error' in stderr:
            raise Exception(stderr)
        info_list = [pr.strip() for pr in stdout.split(',')]
        app_win_list = []
        for info in info_list:
            app_window = list(re.findall(r"window (.*) of application process (.*)",info,re.S)[0])
            app_window.reverse()
            app_window = app_window[0]+'_'+app_window[1]
            app_win_list.append(app_window)
        return app_win_list

    def get_frontmost_window_info(self):
        """获取前台窗口的信息：app名称，窗口标题，窗口坐标和大小"""
        # script = '''
        # tell application "System Events"
        #     set appProc to the first process whose frontmost is true
        # end tell
        # return appProc
        #     '''
        # p = sub.Popen(['osascript', '-e',script], stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
        # stdout, stderr = p.communicate()
        # if 'error' in stderr:
        #     raise Exception(stderr)
        # while stdout.strip()=='application process python':
        #     time.sleep(0.01)
        #     p = sub.Popen(['osascript', '-e', script], stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE,
        #                   universal_newlines=True)
        #     stdout, stderr = p.communicate()
        #     if 'error' in stderr:
        #         raise Exception(stderr)

        script = '''
        tell application "System Events"
            set appProc to the first process whose frontmost is true
            set appWindow to the value of attribute "AXFocusedWindow" of appProc
            set appProcName to the name of appProc
            set appWindowName to the name of appWindow
            set {w, h} to the size of appWindow
            set {x, y} to the position of appWindow
            set appBounds to {x, y, x + w, y + h}
        end tell
        return {appProcName, appWindowName, appBounds}
        '''
        p = sub.Popen(['osascript', '-e',script], stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
        stdout, stderr = p.communicate()
        if 'error' in stderr:
            raise Exception(stderr)
        process_list = [pr.strip() for pr in stdout.split(',')]
        return process_list

    def set_process_frontmost(self, app_name):
        """将进程窗口显示到最前，最小化后没办法打开，推荐使用open_app_and_activate"""
        script = '''
                    tell application "System Events"
                        set frontmost of process "%s" to true
                    end tell
                    ''' % app_name
        p = sub.Popen(['osascript', '-'], stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(script)
        if 'error' in stderr:
            raise Exception(stderr)

    def set_app_window_focus(self,app_name,win_name):
        """打开指定应用窗口并聚焦"""
        script = '''
                    tell application "System Events"
                        tell application "%s"
                            #reopen
                            activate window "%s"
                        end tell
                    end tell
                    ''' % (app_name,win_name)
        p = sub.Popen(['osascript', '-'], stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(script)
        if 'error' in stderr:
            raise Exception(stderr)

    def open_app_and_activate(self, app_name):
        """打开应用并激活显示到最前"""
        script = '''
                    tell application "%s"
                        reopen
                        activate
                    end tell
                    ''' % app_name
        p = sub.Popen(['osascript', '-'], stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(script)
        if 'error' in stderr:
            raise Exception(stderr)
        self.wait_for_app_show(app_name)

    def quit_app(self, app_name):
        app_name = os.path.split(app_name)[1].split('.app')[0]
        """关闭并退出应用"""
        script = '''
                    tell application "%s"
                        quit
                    end tell
                    ''' % app_name
        p = sub.Popen(['osascript', '-'], stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
        stdout, stderr = p.communicate(script)
        if 'error' in stderr:
            raise Exception(stderr)
        #等待应用退出
        while app_name in self.get_all_process():
            time.sleep(0.1)

    def relaunch_app(self, app_name):
        """重启应用"""
        app_name = os.path.split(app_name)[1].split('.app')[0]
        #判断应用是否开启，如果开启，则先关闭退出
        if app_name in self.get_all_process():
            self.quit_app(app_name)
        #开启应用
        self.open_app_and_activate(app_name)

    def click_event(self, app_name, button, position, click_times):
        """
        切换到指定窗口，在指定坐标位置触发鼠标点击事件
        :param app_name: 想要点击的进程名称
        :param button: 点击的按钮："left", "middle", "right",
        :param position: 点击的坐标，如 (100,100)
        :param click_times: 点击的次数，1为单击，2为双击，3为三击，间隔为0
        :return:
        """
        if button=='left':
            button=Button.left
        elif button=='middle':
            button=Button.middle
        elif button=='right':
            button=Button.right
        # 切换到指定窗口
        self.open_app_and_activate(app_name)
        # 移动到指定位置
        pyautogui.moveTo(position[0],position[1])
        # 点击鼠标
        Controller().click(button, click_times)
        # pyautogui.click(x=position[0], y=position[1], clicks=click_times, button=button)

    def input_event(self, app_name, position, input_message):
        """切换到指定应用，在指定坐标位置输入内容"""
        # 鼠标聚焦到指定位置
        self.click_event(app_name, 'left', position, 1)
        # 输入内容
        pyautogui.typewrite(input_message)

    def single_keyboard_event(self, key):
        """单个键键盘点击事件
         ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
        ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
        'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
        'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
        'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
        'browserback', 'browserfavorites', 'browserforward', 'browserhome',
        'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
        'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
        'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
        'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
        'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
        'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
        'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
        'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
        'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
        'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
        'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
        'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
        'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
        'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
        'command', 'option', 'optionleft', 'optionright']
        """
        pyautogui.press(key)

    def commbo_keyboard_event(self, *keys):
        """组合键键盘事件"""
        pyautogui.hotkey(*keys)

    def app_control_event(self,app_control_type,app_path):
        """软件控制事件"""
        if app_control_type=='打开软件':
            self.open_app_and_activate(app_path)
        if app_control_type=='关闭软件':
            self.quit_app(app_path)
        if app_control_type=='重启软件':
            self.relaunch_app(app_path)

    def get_position_rgb(self, app_name, position):
        """获取指定应用窗口某位置的rgb值"""
        # 切换到指定app窗口
        self.open_app_and_activate(app_name)
        # 获取指定位置的rgb值
        im = pyautogui.screenshot(region=(position[0], position[1], 1, 1))
        rgb = im.getpixel((0,0))[0:3]
        return rgb

    def check_positioin_rgb(self, app_name, position, desired_rgb):
        """判断指定应用窗口某位置的rgb值是否与给定值相匹配"""
        rgb = self.get_position_rgb(app_name, position)
        if rgb == desired_rgb:
            return True
        else:
            return False

    def wait_for_app_show(self,app_name):
        """等待窗口显示到最前端"""
        app_name = os.path.split(app_name)[1].split('.app')[0]
        frontmost_app_name = self.get_frontmost_window_info()[0]
        while app_name != frontmost_app_name:
            print(app_name,frontmost_app_name)
            time.sleep(0.1)
            frontmost_app_name = self.get_frontmost_window_info()[0]

    def mouse_scroll_event(self,position,scroll_value):
        """鼠标滚轮的滚动事件
        scroll_value：鼠标滚轮的滚动值
        position：鼠标滚动时的坐标x,y
        """
        pyautogui.scroll(scroll_value,x=position[0],y=position[1])

    def mouse_move_event(self,position):
        """
        鼠标移动事件
        position：鼠标想要移动到的坐标x,y
        """
        pyautogui.moveTo(x=position[0],y=position[1])

    def screenshot_event(self,img_path,region):
        """
        截图事件
        region：所截取图片左上顶点的坐标x,y和所截取图片的宽高w,h，如(0,0,100,100)
        """
        pyautogui.screenshot(imageFilename=img_path,region=region)

    def position_measurement(self):
        """获取鼠标当前位置的坐标"""
        currentMouseX, currentMouseY = pyautogui.position()
        return currentMouseX, currentMouseY

    def rgb_measurement(self):
        """获取当前位置的rgb值"""
        position = self.position_measurement()
        im = pyautogui.screenshot(region=(position[0], position[1], 1, 1))
        rgb = im.getpixel((0,0))[0:3]
        return rgb


if __name__ == '__main__':
    wf = WorkFlow()
    # print(wf.get_all_windows())
    # wf.set_app_window_focus('Terminal','wheels — -bash — 80×24')
    # print(wf.get_all_process())
    # wf.open_app_and_activate('Terminal')
    # print(wf.get_all_windows())
    # wf.quit_app('TextEdit')
    # print(wf.get_all_windows())
    # print(wf.get_frontmost_window_info())
    # wf.relaunch_app('TextEdit')
    # wf.input_event('TextEdit',(None,None),'NiHao')
    # print(wf.position_measurement())
    # print(wf.rgb_measurement())
    # wf.click_event('Finder','left',(214,192),1)
    # pyautogui.doubleClick(214, 192)
    # pyautogui.click(458,846)
    # wf.input_event('Finder',(921,183),'你好')
    # wf.single_keyboard_event('enter')
    # wf.commbo_keyboard_event('command','tab')
    print(wf.get_frontmost_window_info())
