import logging

# 默认情况下,logging 将日志打印到屏幕,日志级别为WARNING
# 日志级别大小关系为
# CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET


# logging.debug("This is debug message")
# logging.info("This is info message")
# logging.warning("This is warning message")

logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s %(asctime)s',
                    datefmt='%Y-%m-%d %X',
                    filename="myapp.txt",
                    filemode="w"
                    )
logging.debug("This is debug message")
logging.info("This is info message")
logging.warning("This is warning message")