(print | copy | get) actions: user.print_copy_actions()
(print | copy | get) captures: user.print_copy_captures()

# Useful when dragon hangs. Say "mic check", it'll ping when it's ready.
(mic | mike) (test | check): user.mic_test()

(copy app | app info): user.copy_current_app_info()

talon (repl | reppull): user.talon_open_repl()
talon user [dir]: user.talon_open_user_dir()
talon [show] log: user.talon_show_log()
