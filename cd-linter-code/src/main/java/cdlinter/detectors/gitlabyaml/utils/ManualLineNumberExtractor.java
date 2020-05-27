package cdlinter.detectors.gitlabyaml.utils;

import cdlinter.detectors.gitlabyaml.entities.GitLabYAML;
import cdlinter.detectors.gitlabyaml.entities.Job;
import cdlinter.detectors.gitlabyaml.entities.When;

public class ManualLineNumberExtractor extends GitLabYAMLLineNumberExtractor {

    public ManualLineNumberExtractor(GitLabYAML gitLabYAML) {
        super(gitLabYAML);
    }

    @Override
    public Boolean categoryIsNotDefault(Job defJob) {
        return defJob.getWhen() == When.manual;
    }

    @Override
    public Boolean jobSameAsDefJob(Job job, Job defJob) {
        return job.getWhen() == defJob.getWhen();
    }
}
