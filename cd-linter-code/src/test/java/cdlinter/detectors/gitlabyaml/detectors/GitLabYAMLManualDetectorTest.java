package cdlinter.detectors.gitlabyaml.detectors;

import cdlinter.antipattern.entities.CIAntiPattern;
import cdlinter.project.entities.LintProject;
import org.junit.BeforeClass;
import org.junit.Test;

import java.util.List;

import static org.junit.Assert.*;

public class GitLabYAMLManualDetectorTest {

    private static LintProject project;
    private static List<CIAntiPattern> antiPatterns;

    @BeforeClass
    public static void setBeforeClass() throws Exception {
        project = new LintProject();
        project.setLocalPath("src/test/resources/gitlabyaml/manual");
        antiPatterns = new GitLabYAMLManualDetector(project).lint();
    }

    @Test
    public void numberOfAntiPatterns() {
        assertEquals(2, antiPatterns.size());
    }
}