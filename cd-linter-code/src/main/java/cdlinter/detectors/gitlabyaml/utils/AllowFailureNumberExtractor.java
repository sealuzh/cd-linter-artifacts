package cdlinter.detectors.gitlabyaml.utils;

import cdlinter.detectors.gitlabyaml.entities.GitLabYAML;
import cdlinter.detectors.gitlabyaml.entities.Job;

public class AllowFailureNumberExtractor extends GitLabYAMLLineNumberExtractor {

    public AllowFailureNumberExtractor(GitLabYAML gitLabYAML) {
        super(gitLabYAML);
    }

    @Override
    public Boolean categoryIsNotDefault(Job defJob) {
        return defJob.getAllow_failure();
    }

    @Override
    public Boolean jobSameAsDefJob(Job job, Job defJob) {
        return job.getAllow_failure() == defJob.getAllow_failure();
    }
}
