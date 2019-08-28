package in.research.utils;

import java.io.IOException;
import java.io.InputStream;
import java.util.logging.LogManager;
import java.util.logging.Logger;

public class Log {

    private java.util.logging.Logger LOGGER;

    public Log() throws IOException {
        InputStream stream = Log.class.getClassLoader().getResourceAsStream("logging.properties");
        LogManager.getLogManager().readConfiguration(stream);
        LOGGER = Logger.getLogger(java.util.logging.Logger.GLOBAL_LOGGER_NAME);
    }

    public void log(String type, Object message) {
        String msg = message.toString() + "::" + System.currentTimeMillis();
        switch (type) {
            case "INFO" : LOGGER.info(msg); break;
            case "WARN" : LOGGER.warning(msg); break;
            case "SEVERE" : LOGGER.severe(msg); break;
        }
    }

}
