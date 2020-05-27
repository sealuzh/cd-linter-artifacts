package cdlinter.detectors.gitlabyaml.utils;

import cdlinter.detectors.gitlabyaml.entities.GitLabYAML;
import cdlinter.detectors.gitlabyaml.entities.Job;
import cdlinter.utils.DefinitionPointer;
import cdlinter.utils.LineNumberExtractor;

import java.util.List;
import java.util.Map;

public abstract class GitLabYAMLLineNumberExtractor {

    protected GitLabYAML gitLabYAML;
    protected LineNumberExtractor lineNumberExtractor;
    protected Map<String, List<String>> pointers;

    public GitLabYAMLLineNumberExtractor(GitLabYAML gitLabYAML) {
        this.gitLabYAML = gitLabYAML;
        this.lineNumberExtractor = new LineNumberExtractor(gitLabYAML.getRaw());
        DefinitionPointer definitionPointer = new DefinitionPointer(gitLabYAML);
        this.pointers = definitionPointer.getPointers();
    }

    public abstract Boolean categoryIsNotDefault(Job defJob);
    public abstract Boolean jobSameAsDefJob(Job job, Job defJob);

    public String getLineNumber(Job job) {
        String jobName = job.getName();
        if (pointers.containsKey(jobName)) {
            for (String def : pointers.get(jobName)) {
                Job defJob = gitLabYAML.getJob(def);
                if (categoryIsNotDefault(defJob)) {
                    if (jobSameAsDefJob(job, defJob)) {
                        return lineNumberExtractor.getLineNumber(defJob.getName()+":");
                    }
                }
            }
        }

        return lineNumberExtractor.getLineNumber(jobName+":");
    }

}
