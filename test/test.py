def _load_toml_config(self) -> None:
        """加载 TOML 配置"""
        try:
            with open(self.config_path, "rb") as f:
                toml_data = tomllib.load(f)
                self.toml_data = toml_data
                self._record_source("toml_data", "_load_config")

                # 加载已知配置节
                fastapi_server_data = toml_data.get("FastAPI_Server", {})
                self.fastapi_server_host = fastapi_server_data.get("fastapi_server_host", None)
                self.fastapi_server_port = fastapi_server_data.get("fastapi_server_port", None)

                napcat_server_data = toml_data.get("Napcat_Server", {})
                self.fastapi_server_host = napcat_server_data.get("napcat_server_host", None)
                self.fastapi_server_host = napcat_server_data.get("napcat_server_port", None)
                self.fastapi_server_host = napcat_server_data.get("napcat_server_token", None)

        except Exception as e:
            raise ConfigError(f"TOML 配置解析失败: {e}")

CONFIG = [
        "fastapi_server_host",
        "fastapi_server_port",
        "napcat_server_host",
        "napcat_server_port",
        "napcat_server_token"
    ]
