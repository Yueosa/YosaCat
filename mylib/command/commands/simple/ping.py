from ...decorators import simple_command


@simple_command("/ping")
def ping():
    print("pong!")