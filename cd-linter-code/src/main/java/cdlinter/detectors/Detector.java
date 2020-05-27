package cdlinter.detectors;

import cdlinter.antipattern.entities.CIAntiPattern;
import cdlinter.project.entities.LintProject;

import java.util.List;

public abstract class Detector {

    protected LintProject project;

    public Detector(LintProject project) {
        this.project = project;
    }

    public abstract List<CIAntiPattern> lint() throws Exception;

    public static String removeIllegalCharsInID(String id) {
        return id.replaceAll("[ <>#%\"{}|^'`;\\[\\]/?:@&=+$,.()\\\\]", "-");
    }
}
