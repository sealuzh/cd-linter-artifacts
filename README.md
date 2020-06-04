# CD-Linter Artifacts

This is the replication package of the paper "[Configuration Smells in Continuous Delivery Pipelines: A Linter and A Six-Month Study on GitLab](https://doi.org/10.5281/zenodo.3860984)" accepted for publication at [ESEC/FSE 2020](https://2020.esec-fse.org/).

In the following, we describe the artifacts of our paper and how to use them to replicate the results of our study. When appropriate, we also link the description of the artifacts to the relevant sections in the paper.

## Environment Set-up

Follow the instructions described in [INSTALL.md](INSTALL.md). 

**Note** To successfully run all scripts listed in this document, you need to keep the root of this repository as your working directory. An internet connection is required.

## <a id="cd-linter"></a>Build and Run CD-Linter

CD-Linter is a semantic linter for GitLab CI/CD pipelines. It downloads and checks the configuration files (e.g., _.gitlab-ci.yml_, _pom.xml_, _requirements.txt_ files) of open-source projects that are hosted on GitLab.com for the presence of four CD smells (see Section 3.2). 

CD-Linter has been implemented in Java and its source code is available in the `cd-linter` folder. To detect smells, CD-Linter accepts as inputs:

* the list of projects (see `cd-smell-occurrences/dataset.csv`)
* the path to the folder where configuration files are cached
* the path to the resulting file that will contain all detected smells.

To build and execute CD-Linter, please run:

	mvn -f cd-linter clean test exec:java -Dexec.mainClass="ch.uzh.seal.app.ConfigurationAnalytics" -Dexec.args="cd-smell-occurrences/dataset.csv cd-smell-occurrences/linter_configfiles cd-linter/target/cd-smells.csv"
	
The `cd-smell-occurrences/dataset.csv` file contains the list of projects that have been analyzed in our study (see Section 4.1). The `cd-smell-occurrences/linter_configfiles` folder includes the latest version of the configuration files used to measure the CD-smell occurrences in RQ3 (see Section 4.4).
<!--- The resulting `cd-linter/CI-anti-patterns.csv` file corresponds to `cd-smell-occurrences/rq3-results.csv`.-->

### Query GitLab projects and Download Configuration Files

While its primary goal is to detect CD smells, CD-Linter provides another functionality for the purposes of our study. It mines the full list of open-source projects available on GitLab.com together with some basic statistics such as the languages, number of stars and forks.

To try this feature, please execute<sup>1</sup>: <mark>**TODO**: Add a valid token that possibly expires soon</mark>

	mvn clean test exec:java -Dexec.mainClass="ch.uzh.seal.datamining.gitlab.GitLabMiner" -Dexec.args="$TOKEN $OUTPUT 0"

<!-- The execution returns a file having the same structure of `cd-smell-occurrences/dataset.csv`. -->

<sup>1</sup> Note that a full analysis of the GitLab ecosystem takes weeks.

<!--- ## Construction of the original dataset

We applied several filters from a broad GitLab query to construct a dataset consisting of 5,312 projects.-->

## Analysis of the Reactions to the Opened Issues (RQ1)

<!--- ### Selection of the issues to open

We detected smells on the latest versions of the selected projects available at <mark>XX</mark>. From the resulting 5,312 smells we selected a sample of 168 smells to open applying several filters. During the assessment stage, we discarded 23 from this set and finally open 145 issues. The full list of issues together with the reactions is available at `XX.csv`.-->


All the reactions to the opened-issues (see Section 4.2) have been collected in the `reactions-to-issues/rq1-cd-smells.csv` file. Among the others, each line contains the following information<sup>2</sup>:

*  link to the issue (_linkToOpenedIssue_)
*  status of the reported smell (_fixed_)
*  reaction to the issue (_reaction_)
*  number of upvotes (_numUpvotes_), downvotes (_numDownvotes_), and comments (_numComments_)
*  status of the issue (_state_)
*  assignment to team members (_isAssigned_)
*  resolution time in ms (_resolution-time_)

Taking this file as input, please execute the following command to replicate the analysis performed in RQ1.

	python3 reactions-to-issues/rq1-analysis.py reactions-to-issues/rq1-cdsmells.csv reactions-to-issues/fig4-source.csv > reactions-to-issues/rq1-results.txt

The generated output `reactions-to-issues/rq1-results.txt` contains (i) an analysis of the received reactions, (ii) the labels assigned to the rejected issues with their occurrences, and (iii) the resolution type per CD smell.

The previous script requires a second argument `reactions-to-issues/fig4-source.csv`. This is the path to the file that will store the reactions to the issues in a format that can be processed by the following script to generate `reactions-to-issues/figure4.png` <mark>**TODO**: Add Missing Dependency in Dockerfile</mark>

	Rscript reactions-to-issues/likert-scaled-reactions.R

<sup>2</sup> The last update was done on 05/02/2020.

### Card-sorting of the Received Comments

Two authors performed an independent tagging of the comments that we received in the opened issues and then merged their annotations. The folder `reactions-to-issues/rq1-comment-sorting` contains the labels (`card-sorting-labels.csv`) and the result of the agreement (`card-sorting-agreement.csv`)
		
## Accuracy of CD-Linter (RQ2)

The results of the manual validation of CD smells (see Section 4.3) are available in the `accuracy/rq2-precision.csv` and `accuracy/rq2-recall.csv` files.

The first file, that we used to compute the precision of our tool, contains a sample of detected CD smells together with the final tag (or rating) assigned by the validators. The `accuracy/rq2-recall-sample.csv` file contains instead the list of projects inspected for the recall analysis of CD-Linter. We compared the list of manually identified smells with the ones detected by CD-Linter in `accuracy/rq2-recall.csv`. Specifically, given a manually identified smell, the column _match with cd-linter_ contains _YES_ if the smell was also detected by CD-Linter.

To compute the results shown in Tables 2 and 3 and the recall values (see Section 5.2), please run:

	python3 accuracy/rq2-analysis.py accuracy/rq2-precision.csv accuracy/rq2-recall.csv > accuracy/rq2-results.txt


### Generate a Random Sample to Compute the Recall

We generated a random sample of 100 projects to compute the recall. Specifically, we excluded projects having smells analyzed while studying the precision and contained in the opened issues. To generate such a random sample (and store it in `accuracy/generated-sample.csv`), please run:

	python3 accuracy/rq2-recall-sample.py cd-smell-occurrences/dataset.csv accuracy/rq2-precision.csv reactions-to-issues/rq1-cdsmells.csv accuracy/generated-sample.csv

<!-- After incorporating a few feedback in our tool, we rerun it and detected 5,011 smells. We then evaluated CD-Linter's precision and recall measures.

### Selection of smells for precision

Applying several filters (see Section XX), we selected 868 smells to evaluate. The results are available in `hello.csv`. -->

## Occurrences of CD smells (RQ3)

We run CD Linter against the latest snapshot of the projects that were still available at the end of the six-month study (as already described in [Build and Run CD-Linter](#cd-linter)). The results are available at `cd-smell-occurrences/rq3-results.csv`.

To compute the results (that are described in Section 5.3), please run:

	python3 cd-smell-occurrences/rq3-analysis.py cd-smell-occurrences/dataset_yml-update.csv cd-smell-occurrences/rq3-cd-smells.csv > cd-smell-occurrences/rq3-results.txt


### Compute the size of .gitlab-ci.yml files

You might have noticed that the previous script takes `dataset_yml-update.csv` instead of `dataset.csv`. This file is required for the analysis of CD smells across different .gitlab-ci.yml sizes (see Table 5). To generate it please run the following command.

	mvn -f cd-linter clean test exec:java -Dexec.mainClass="ch.uzh.seal.app.ConfigurationMiner" -Dexec.args="cd-smell-occurrences/dataset.csv cd-smell-occurrences/linter_configfiles cd-linter/target/dataset_yml-update.csv"

## Others

### Bad practices in CI/CD

All the good and bad practices that we collected from the _Foundations_ part of Humble's and Farley's book<sup>3</sup> are collected in `good-bad-cd-practices.csv`.

<sup>3</sup> https://www.oreilly.com/library/view/continuous-delivery-reliable/9780321670250/