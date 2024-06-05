import law
import law.contrib
import time
import collections
import law.contrib.tasks
from functools import wraps
from law.parameter import NotifyParameter
from law.contrib.slack.notification import notify_slack
from law.decorator import notify
from law.util import human_duration

law.contrib.load("tasks")

class NotifySlackParameterUTF8(NotifyParameter):

    def __init__(self, *args, **kwargs):
        super(NotifySlackParameterUTF8, self).__init__(*args, **kwargs)
        
        self.init_time = None
        self.end_time = None

        if not self.description:
            self.description = "when true, and the task's run method is decorated with " \
                "law.decorator.notify, a Slack notification is sent once the task finishes"

    @staticmethod
    def notify(success, title, content, **kwargs):
        print(success, title, content, kwargs)
        # escape the full content
        content = content.__class__(
            (k, v if isinstance(v, str) else v)
            for k, v in content.items()
        )

        # overwrite title with slack markdown markup
        title = "*Notification from* `{}`".format(content["Task"])
        del content["Task"]
        
        # overwrite duration with custom
        start_time = kwargs.get('start_time', None)
        end_time = kwargs.get('end_time', None)
        if start_time is not None:
            duration = time.time() - start_time
            # Make this a readable time
            content["Duration"] = human_duration(seconds=duration)

        # markup for traceback
        if "Traceback" in content:
            content["Traceback"] = "```{}```".format(content["Traceback"])

        # prepend the status text to the message content
        # emojis are "party popper" and "exclamation mark"
        parts = list(content.items())
        status_text = "success \U0001F389" if success else "failure \U00002757"
        parts.insert(0, ("Status", status_text))
        content = collections.OrderedDict(parts)

        # attachment color depends on success
        color = "#4bb543" if success else "#ff0033"

        # send the notification
        return notify_slack(title, content, attachment_color=color, **kwargs)

    def get_transport(self):
        return {
            "func": self.notify,
            "raw": True,
            "colored": False,
        }

# TODO document
class SplitTimeDecorator:
    def __init__(self):
        self.start_time = None

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.start_time is None:
                self.start_time = time.time()
            if func.__name__ != 'run':
                result = func(*args, **kwargs)
            else:
                result = notify(start_time=self.start_time)(func)(*args, **kwargs)
            return result

        return wrapper

class NotifTest(law.tasks.RunOnceTask):

    notify_slack = NotifySlackParameterUTF8()
    split_timer = SplitTimeDecorator()
    
    @split_timer
    def requires(self):
        print('running reqs')
        return None
    
    @split_timer
    def run(self):
        print('running run')
        time.sleep(2)
