import logging


def root_logger():
    # root loggerを取得
    logger = logging.getLogger(__name__)

    class ColorfulHandler(logging.StreamHandler):
        def emit(self, record: logging.LogRecord) -> None:
            mapping = {
                "TRACE": "trace",
                "DEBUG": "\x1b[0;36mDEBUG\x1b[0m",
                "INFO": "\x1b[0;32mINFO\x1b[0m",
                "WARNING": "\x1b[0;33mWARNING\x1b[0m",
                "WARN": "\x1b[0;33mWARN\x1b[0m",
                "ERROR": "\x1b[0;31mERROR\x1b[0m",
                "ALERT": "\x1b[0;37;41mALERT\x1b[0m",
                "CRITICAL": "\x1b[0;37;41mCRITICAL\x1b[0m",
            }

            record.levelname = mapping[record.levelname]
            super().emit(record)

    if not logger.hasHandlers():
        # formatterを作成
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s (%(filename)s)')

        # handlerを作成しフォーマッタを設定，loggerにhandlerを設定
        # ストリームハンドラ
        stream_handler = ColorfulHandler()  # ストリームハンドラの作成
        stream_handler.setFormatter(formatter)  # フォーマッタを設定
        logger.addHandler(stream_handler)  # loggerにhandlerを設定
        # ファイルハンドラ
        # file_handler = logging.FileHandler('log.txt')  # ストリームハンドラの作成
        # file_handler.setFormatter(formatter)  # フォーマッタを設定
        # logger.addHandler(file_handler)  # loggerにhandlerを設定

        # log levelを設定
        logger.setLevel(logging.DEBUG)

    return logger
