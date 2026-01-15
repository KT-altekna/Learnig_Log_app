import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    # ログレベル
    log_level = logging.DEBUG if app.debug else logging.INFO

    app.logger.setLevel(log_level)

    # フォーマット
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

    # コンソール出力（開発・Render両対応）
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)

    if not app.logger.handlers:
        app.logger.addHandler(stream_handler)

    # ファイル出力（本番のみ・任意）
    if not app.debug:
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        file_handler = RotatingFileHandler(
            f"{log_dir}/app.log",
            maxBytes=1024 * 1024,
            backupCount=5
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
