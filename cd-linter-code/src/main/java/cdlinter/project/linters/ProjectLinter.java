package cdlinter.project.linters;

import cdlinter.antipattern.entities.CIAntiPattern;
import cdlinter.detectors.gitlabyaml.detectors.GitLabYAMLAllowFailureDetector;
import cdlinter.detectors.gitlabyaml.detectors.GitLabYAMLManualDetector;
import cdlinter.detectors.gitlabyaml.detectors.GitLabYAMLRetryDetector;
import cdlinter.detectors.maven.versioning.MavenVersionAntiPatternDetector;
import cdlinter.detectors.python.versioning.PythonVersionAntiPatternDetector;
import cdlinter.project.entities.LintProject;

import java.util.ArrayList;
import java.util.List;

public class ProjectLinter {

    public static List<CIAntiPattern> getCIAntiPatterns(LintProject lintProject) throws Exception {
        List<CIAntiPattern> antiPatterns = new ArrayList<>();

        String language = lintProject.getLanguage();
        String buildTool = lintProject.getBuildToolName();

        if (buildTool.equals("Maven")) {
            antiPatterns.addAll(new MavenVersionAntiPatternDetector(lintProject).lint());
        }
        else if (language.equals("Python")) {
            antiPatterns.addAll(new PythonVersionAntiPatternDetector(lintProject).lint());
        }
        
        //antiPatterns.addAll(new GitLabYAMLDuplicateLibraries(lintProject).lint());

        antiPatterns.addAll(new GitLabYAMLAllowFailureDetector(lintProject).lint());
        antiPatterns.addAll(new GitLabYAMLRetryDetector(lintProject).lint());
        //antiPatterns.addAll(new GitLabYAMLVulnerabilityDetector(lintProject).lint());
        antiPatterns.addAll(new GitLabYAMLManualDetector(lintProject).lint());
        //antiPatterns.addAll(new GitLabYAMLOnlyExceptDetector(lintProject).lint());

        return antiPatterns;
    }
}
