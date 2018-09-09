#!/usr/bin/python3
# _*_ coding: utf-8 _*_

import sys
import os
import bfcm

class App:

    def run(self):
        args = sys.argv
        if len(args) < 3:
            sys.stderr.write('usage:%s %s %s\n' % (args[0], 'command', 'config_path'))
            return 1
        command = args[1]
        config = args[2]
        if not os.path.exists(config):
            sys.stderr.write('設定ファイルが見つかりません: %s\n' % args[2])
            return 2
        cg = bfcm.logic.ConfigLogic()
        cm = cg.create_config_manager(config)
        commander = bfcm.commander.Commander(cm)
        commander.execute(command, args[3:])
        return 0

if __name__ == '__main__':
    app = App()
    sys.exit(app.run())
