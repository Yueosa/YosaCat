# FastAPI 启动入口
    # - 接收 OneBot 推送的所有事件（message、notice、meta_event 等）
    # - 调用 Parser 层完成数据解析
    # - 调用 Dispatcher 分发给具体的消息处理器
import uvicorn
from fastapi import FastAPI, Request

from mylib import Cerebrum


class Yosa:
    def __init__(self,app: FastAPI):
        self.app = app
        self.crm = Cerebrum()
        self._register_routes(self.app)
    
    def _register_routes(self, app: FastAPI):
        @app.post("/")
        async def stm_msg(request: Request):
            data = await request.json()
            # print("接收到:", data)
            self.crm.command_mind(data)
            return {}


if __name__ == "__main__":
    app = FastAPI()
    yosa = Yosa(app)
    uvicorn.run(app, port=8080, host="0.0.0.0")
