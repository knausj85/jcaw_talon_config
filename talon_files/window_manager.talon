(minimize | mini): app.window_hide()
(maximize | maxi): user.maximize()
quit program: app.window_close()
(next | neck) (window | win): app.window_next()
(last | larse) (window | win): app.window_previous()
(new | open) (window | win): app.window_open()
[show] programs: user.all_programs()
fullscreen: user.toggle_fullscreen()

(focus | cooss | kiss | cuss | curse) <user.running_applications>:
    user.switcher_focus(running_applications)
(list | show) running: user.switcher_list_running()
(kill | close | hide) running: user.switcher_hide_running()
