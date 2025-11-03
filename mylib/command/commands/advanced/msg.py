from ...decorators import command, argument
from ...base import BaseCommand


@argument("-i", "--id", int, True)
@argument("-m", "--message", str, True)
@command(name="msg", description="发送消息")
class MsgCommand(BaseCommand):
    def execute(self):
        obj = self.get('-i', '--id')
        msg = self.get('-m', '--message')
        print(f"📨 发送到 {obj} : {msg}")
