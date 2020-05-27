package cdlinter.detectors.gitlabyaml.detectors;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import cdlinter.detectors.gitlabyaml.entities.GitLabYAML;
import cdlinter.detectors.gitlabyaml.entities.Job;
import cdlinter.detectors.gitlabyaml.parsers.GitLabYAMLParser;
import cdlinter.detectors.Detector;
import cdlinter.project.entities.LintProject;

abstract class GitLabYAMLDetector extends Detector {

	GitLabYAMLDetector(LintProject project) {
		super(project);
	}

	GitLabYAML getGitLabYAML(LintProject project) {
		String yamlContent = project.getFileContent(".gitlab-ci.yml");
		GitLabYAMLParser parser = new GitLabYAMLParser();
		GitLabYAML yaml = parser.parse(yamlContent);

		ArrayList<String> include = yaml.getInclude();
		// System.out.println(include.size());
		for(String path: include) {
			if(!path.startsWith("/"))
				path = "/"+ path;

			System.out.println(path);
			String depYamlContent = project.getRemoteFileOnly(path);
			// System.out.println(depYamlContent);
			GitLabYAMLParser depParser = new GitLabYAMLParser();
			GitLabYAML depYaml = depParser.parse(depYamlContent);

			Map<String, Job> jobs = depYaml.getJobs();
			// System.out.println(jobs.keySet().size());
			List<String> stages = depYaml.getStages();
			Map<String, String> variables = depYaml.getVariables();


			for(String key: jobs.keySet()) {
				if(!yaml.getJobs().keySet().contains(key)) {
					yaml.addJob(key, jobs.get(key));}
			}

			for(String s: stages) {
				if(!yaml.getStages().contains(s)) {
					yaml.addStage(s);}
			}

			for(String key : variables.keySet()) {
				if(!yaml.getVariables().keySet().contains(key)) {
					yaml.addVariable(key, variables.get(key));}
			}
		}

		return yaml;

	}
}
