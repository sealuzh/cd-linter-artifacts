package cdlinter.utils;

public class LineNumberPathConstructor {

    public static String getPath(String path, String lineNumber) {
        return path + "#L" + lineNumber;
    }
}
