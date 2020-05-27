import numpy as np
import pandas
import random
import re
from scipy.stats import pearsonr, spearmanr


# ausiliary functions

def buildSeriesByCategory(df, categories):
    res = []
    for cat in categories:
        occ = df.loc[df["category"] == cat].shape[0]
        res.append(occ)
    res_series = pandas.Series(res, index=categories)
    return res_series


# convert dataframe that can be used to generate likert plot
def convertToRLikertFormat(dataframe):
    # get rows from dataframe
    version_series = dataframe.loc["Versioning"]
    manual_series = dataframe.loc["Manual-Job"]
    retry_series = dataframe.loc["Job-Retry"]
    allow_series = dataframe.loc["Job-Allow-Failure"]
    overall_series = dataframe.loc["overall"]

    # convert to R format and fill the dictionary
    dict_of_columns = {}
    dict_of_columns['Fuzzy Version'] = fillList(version_series)
    dict_of_columns['Manual Execution'] = fillList(manual_series)
    dict_of_columns['Retry Failure'] = fillList(retry_series)
    dict_of_columns['Fake Success'] = fillList(allow_series)
    dict_of_columns['Overall'] = fillList(overall_series)

    # merge everything in one dataframe
    result = pandas.DataFrame(dict_of_columns)
    return result


def fillList(series):
    list = []
    for label, value in series.items():
        if label != "reacted":
            num = value
            while num > 0:
                list.append(label)
                num = num - 1
    return pandas.Series(list)


def printStatsByCategory(df, categories):
    for cat in categories:
        occ = df.loc[df["category"] == cat].shape[0]
        print(cat + ": " + str(occ))


def buildOverallResultSeries(resulting_series):
    res_list = []
    for label, serie in resulting_series.items():
        sum = 0;
        for value in serie:
            sum += value
        res_list.append(sum)
    return res_list


def fillTwoLists(typ, cat, labels_string, cat_list, label_list):
    labels = labels_string.split(",")
    for label in labels:
        if label != 'nan':
            cat_list.append(cat)
            label_list.append(typ + ":" + label.strip())


def computeProjectSet(list, splitRule, categories):
    resulting_set = set()
    base_link = "https://gitlab.com"

    for name in list:
        if splitRule != "":
            splittedName = name.split(splitRule)

            new_name = base_link

            for token in splittedName:
                if token in categories:
                    break
                else:
                    token = re.sub(r"[ <>#%\"{}|^'`;\[\]/?:@&=+$,\.()\\\\]", my_replace, token)
                    new_name += "/" + token
            resulting_set.add(new_name)

    return resulting_set


def my_replace(match):
    return "-"


def recallSample(start_data_file, rqone_file, rqtwo_file, output_file, categories):
    with open(start_data_file) as dataset_reader, open(rqone_file) as rqone_reader, open(rqtwo_file) as rqtwo_reader:
        dataset = pandas.read_csv(dataset_reader)
        # hasYaml	hasRequirements	hasPoms
        dataset = dataset.loc[dataset['hasYaml']]
        rqone = pandas.read_csv(rqone_reader)
        rqtwo = pandas.read_csv(rqtwo_reader)

        dataset_len = dataset.shape[0]
        rqone_len = rqone.shape[0]
        rqtwo_len = rqtwo.shape[0]
        print("Dataset's size: " + str(dataset_len))
        print("RQ1's size: " + str(rqone_len))
        print("RQ2's size: " + str(rqtwo_len))

        header = dataset.shape[0]
        dataset_proj = dataset['project']
        rqone_proj = rqone['id']
        rqtwo_proj = rqtwo['ID']

        # note that in RQ2 some issues (of different type) belong to the same project and some project are shared by
        # RQ1 and RQ2
        dataset_set = computeProjectSet(dataset_proj, "/", categories)
        rqone_set = computeProjectSet(rqone_proj, "__", categories)
        rqtwo_set = computeProjectSet(rqtwo_proj, "__", categories)
        print("Dataset's size (unique): " + str(len(dataset_set)))
        print("RQ1's size (unique): " + str(len(rqone_set)))
        print("RQ2's size (unique): " + str(len(rqtwo_set)))

        # compute the candidate set
        d0 = dataset_set.difference(rqone_set)
        print("d0 (dataset - RQ1): " + str(len(d0)))
        # print(d0)
        d1 = d0.difference(rqtwo_set)
        print("d1 (d0 - RQ2): " + str(len(d1)))
        # print(d1)
        print("---")

        # compute the recall sample and save it
        sample_size = 8
        recall_sample = random.sample(d1, sample_size)
        recall_projects = {'project': recall_sample}
        recall_df = pandas.DataFrame(recall_projects)
        recall_df.to_csv(output_file, index=False)

    return


def printOccurrences(antipatterns, tot_smells, tot_ana_projects, tot_ana_owners):
    num_smells = antipatterns['ID'].shape[0]
    percentage_num_smells = round(num_smells / tot_smells * 100, 1)
    print("#smells: " + str(num_smells) + "(" + str(percentage_num_smells) + "%)")

    num_smelly_projects = antipatterns['Project'].unique().shape[0]
    percentage_num_smelly_projects = round(num_smelly_projects / tot_ana_projects * 100, 1)
    print("#smelly-projects: " + str(num_smelly_projects) + "(" + str(percentage_num_smelly_projects) + "%)")

    num_smelly_owners = antipatterns['Owner'].unique().shape[0]
    percentage_num_smelly_owners = round(num_smelly_owners / tot_ana_owners * 100, 1)
    print("#smelly-owners: " + str(num_smelly_owners) + "(" + str(percentage_num_smelly_owners) + "%)")


def printOccurrencesPerCluster(apdf, tot_smells, tot_ana_projects, tot_ana_owners, tot_ana_projects_versioning,
                               tot_ana_owners_versioning):
    print("\n-> Versioning")
    versioning = apdf.loc[apdf["Category"] == "Versioning"]
    printOccurrences(versioning, tot_smells, tot_ana_projects_versioning, tot_ana_owners_versioning)

    print("\n-> Job-Allow-Failure")
    allow_failure = apdf.loc[apdf["Category"] == "Job-Allow-Failure"]
    printOccurrences(allow_failure, tot_smells, tot_ana_projects, tot_ana_owners)

    print("\n-> Job-Retry")
    retry = apdf.loc[apdf["Category"] == "Job-Retry"]
    printOccurrences(retry, tot_smells, tot_ana_projects, tot_ana_owners)

    print("\n-> Manual-Job")
    manual = apdf.loc[apdf["Category"] == "Manual-Job"]
    printOccurrences(manual, tot_smells, tot_ana_projects, tot_ana_owners)


def printOccurrences2(df, tot):
    num_smells = df['ID'].shape[0]
    percentage_num_smells = round(num_smells / tot * 100, 1)
    print("#smells: " + str(num_smells) + "(" + str(percentage_num_smells) + "%)")


def printOccurrencesPerCluster2(apdf, tot_versioning, tot_allow, tot_retry, tot_manual):
    print("-> Versioning")
    versioning = apdf.loc[apdf["Category"] == "Versioning"]
    printOccurrences2(versioning, tot_versioning)

    print("-> Job-Allow-Failure")
    allow_failure = apdf.loc[apdf["Category"] == "Job-Allow-Failure"]
    printOccurrences2(allow_failure, tot_allow)

    print("-> Job-Retry")
    retry = apdf.loc[apdf["Category"] == "Job-Retry"]
    printOccurrences2(retry, tot_retry)

    print("-> Manual-Job")
    manual = apdf.loc[apdf["Category"] == "Manual-Job"]
    printOccurrences2(manual, tot_manual)


def recall_computation(file):
    df = pandas.read_csv(file)
    TTP = df.loc[(df["manual validation"] == "YES")]
    TP = TTP.loc[TTP["match with cd-linter"] == "YES"]
    print(TTP.shape[0])
    print(TP.shape[0])
    rec = round(TP.shape[0] / TTP.shape[0], 2)
    print(rec)


# RQ3 data analysis
def rqthree_results(input_file, dataset):
    datasetf = pandas.read_csv(dataset)
    datasetf = datasetf.loc[datasetf["hasYaml"]]  # remove projects without yaml
    print("Analyzable projects: " + str(datasetf.shape[0]))

    print("\n### Describe dataset ###")
    summary = datasetf['yml_size'].describe()
    tot_projects = datasetf["project"].unique().shape[0]
    tot_owners = datasetf["owner"].unique().shape[0]
    print("Analyzable repositories: " + str(tot_projects))

    # for versioning different candidates
    versioning_candidates = datasetf.loc[(datasetf["language"] == "Python") | (datasetf["hasPoms"])]
    tot_projects_versioning = versioning_candidates["project"].unique().shape[0]
    tot_owners_versioning = versioning_candidates["owner"].unique().shape[0]
    print("Analyzable repositories (Versioning): " + str(tot_projects_versioning))
    print("Analyzable owners: " + str(tot_owners))
    print("Analyzable owners (Versioning): " + str(tot_owners_versioning))
    yml_first_quartile = summary["25%"]
    print("YML-size (25%): " + str(yml_first_quartile))
    yml_third_quartile = summary["75%"]
    print("YML-size (75%): " + str(yml_third_quartile))

    # Merge antipatterns with dataset
    antipatterns = pandas.read_csv(input_file)
    apdf = pandas.merge(antipatterns, datasetf, left_on='Repository Name', right_on='project', how='left')

    # exclude additional python projects without yaml
    apdf = apdf.loc[pandas.notna(apdf["project"])]

    print("\n### Full-analysis of smells ###")

    print("-> Overall")
    tot_smells = apdf['ID'].shape[0]
    tot_smelly_projects = apdf['Project'].unique().shape[0]
    tot_smelly_owners = apdf['owner'].unique().shape[0]
    print("#smells: " + str(tot_smells))
    print("#smelly-projects: " + str(tot_smelly_projects))
    print("#smelly-owners: " + str(tot_smelly_owners))

    printOccurrencesPerCluster(apdf, tot_smells, tot_projects, tot_owners, tot_projects_versioning,
                               tot_owners_versioning)

    print("\n### YAML-size-based clustering analysis ###")
    tot_versioning = apdf.loc[apdf["Category"] == "Versioning"].shape[0]
    tot_allow = apdf.loc[apdf["Category"] == "Job-Allow-Failure"].shape[0]
    tot_manual = apdf.loc[apdf["Category"] == "Manual-Job"].shape[0]
    tot_retry = apdf.loc[apdf["Category"] == "Job-Retry"].shape[0]

    print("\n-> Projects (small yaml)")
    apdf_small = apdf.loc[apdf["yml_size"] <= yml_first_quartile]
    printOccurrences(apdf_small, tot_smells, tot_smelly_projects, tot_smelly_owners)
    printOccurrencesPerCluster2(apdf_small, tot_versioning, tot_allow, tot_retry, tot_manual)

    print("\n-> Projects (medium yaml)")
    apdf_medium = apdf.loc[(apdf["yml_size"] > yml_first_quartile) & (apdf["yml_size"] < yml_third_quartile)]
    printOccurrences(apdf_medium, tot_smells, tot_smelly_projects, tot_smelly_owners)
    printOccurrencesPerCluster2(apdf_medium, tot_versioning, tot_allow, tot_retry, tot_manual)

    print("\n-> Projects (long yaml)")
    apdf_big = apdf.loc[apdf["yml_size"] >= yml_third_quartile]
    printOccurrences(apdf_big, tot_smells, tot_smelly_projects, tot_smelly_owners)
    printOccurrencesPerCluster2(apdf_big, tot_versioning, tot_allow, tot_retry, tot_manual)

    print("\n### YAML-size-based clustering analysis (Big YAML) ###")

    # reduce starting dataset to the high sample
    big_datasetf = datasetf.loc[datasetf["yml_size"] >= yml_third_quartile]
    big_tot_projects = big_datasetf["project"].unique().shape[0]
    big_tot_owners = big_datasetf["owner"].unique().shape[0]
    print("Analyzable repositories: " + str(big_tot_projects))

    # for versioning different candidates
    big_versioning_candidates = big_datasetf.loc[(big_datasetf["language"] == "Python") | (big_datasetf["hasPoms"])]
    big_tot_projects_versioning = big_versioning_candidates["project"].unique().shape[0]
    big_tot_owners_versioning = big_versioning_candidates["owner"].unique().shape[0]
    print("Analyzable repositories (Versioning): " + str(big_tot_projects_versioning))
    print("Analyzable owners: " + str(big_tot_owners))
    print("Analyzable owners (Versioning): " + str(big_tot_owners_versioning))

    big_tot_smells = apdf_big['ID'].shape[0]
    big_tot_smelly_projects = apdf_big['Project'].unique().shape[0]
    big_tot_smelly_owners = apdf_big['Owner'].unique().shape[0]
    print("#smells: " + str(big_tot_smells))
    print("#smelly-projects: " + str(big_tot_smelly_projects))
    print("#smelly-owners: " + str(big_tot_smelly_owners))

    printOccurrencesPerCluster(apdf_big, big_tot_smells, big_tot_projects, big_tot_owners, big_tot_projects_versioning,
                               big_tot_owners_versioning)

    print("\n# Analysis of versioning issues")

    vapdf = apdf.loc[apdf["Category"] == "Versioning"]  # the versioning frame

    # tot incidents per file
    print("\n-> overall")
    versioning_occurrences_byfile(vapdf)

    print("\n-> missing")
    missing = vapdf.loc[vapdf["Sub-Category"] == "missing"]
    versioning_occurrences_byfile(missing)
    print("\n-> only-major-number")
    only_major_number = vapdf.loc[vapdf["Sub-Category"] == "only-major-number"]
    versioning_occurrences_byfile(only_major_number)
    print("\n-> any-minor-number")
    any_minor_number = vapdf.loc[vapdf["Sub-Category"] == "any-minor-number"]
    versioning_occurrences_byfile(any_minor_number)
    print("\n-> any-upper-version")
    any_upper_version = vapdf.loc[vapdf["Sub-Category"] == "any-upper-version"]
    versioning_occurrences_byfile(any_upper_version)

    return


def versioning_occurrences_byfile(smell):
    tot_incidents = smell.shape[0]
    affected_files = smell["Remote Configuration File Link"].unique().shape[0]

    yml_incidents = smell.loc[smell["Configuration File Name"] == ".gitlab-ci.yml"]
    tot_yml_incidents = yml_incidents.shape[0]
    tot_affected_yml = yml_incidents["Remote Configuration File Link"].unique().shape[0]

    req_incidents = smell.loc[smell["Configuration File Name"] == "requirements.txt"]
    tot_req_incidents = req_incidents.shape[0]
    tot_affected_req = req_incidents["Remote Configuration File Link"].unique().shape[0]

    pom_incidents = smell.loc[(smell["Configuration File Name"] != ".gitlab-ci.yml") &
                              (smell["Configuration File Name"] != "requirements.txt")]
    tot_pom_incidents = pom_incidents.shape[0]
    tot_affected_pom = pom_incidents["Remote Configuration File Link"].unique().shape[0]

    print("tot_incidents: " + str(tot_incidents))
    print("affected_files: " + str(affected_files))
    print("tot_yml_incidents: " + str(tot_yml_incidents) + "(" + str(
        round(tot_yml_incidents / tot_incidents * 100, 2)) + "%)")
    print("affected_yml_files: " + str(tot_affected_yml))
    print("tot_req_incidents: " + str(tot_req_incidents) + "(" + str(
        round(tot_req_incidents / tot_incidents * 100, 2)) + "%)")
    print("affected_req_files: " + str(tot_affected_req))
    print("tot_pom_incidents: " + str(tot_pom_incidents) + "(" + str(
        round(tot_pom_incidents / tot_incidents * 100, 2)) + "%)")
    print("affected_pom_files: " + str(tot_affected_pom))


# RQ1 data analysis
def rqone_results(issueReportFile, path):

    with open(issueReportFile) as input_file:
        frame = pandas.read_csv(input_file)  # read file in a dataframe

        tot_opened_issues = frame.loc[pandas.notna(frame["category"]) &
                                      (frame["category"] != "Vulnerability") &
                                      (frame["category"] != "Job-Retry (duplicate)")].shape[0]
        print("### Tot opened issues: " + str(tot_opened_issues))

        # select only active projects
        df = frame.loc[(frame["commitsSinceIssue"] >= 1) &
                       (frame["category"] != "Vulnerability") &
                       pandas.notna(frame["category"]) &
                       (frame["category"] != "Job-Retry (duplicate)")]

        categories = df.category.unique()

        print("\n#### Opened issues (active projects since September 2019) ####")
        openend_series = buildSeriesByCategory(df, categories)
        printStatsByCategory(df, categories)
        activeProjects = df.shape[0]
        print("Total: " + str(activeProjects) + " (" +
              str(tot_opened_issues - activeProjects) + " inactive)")

        print("\n#### Issues (with a reaction) ####")
        # select rows by column values
        react_df = df.loc[(df["fixed (y/n/m)"] == "y") |
                          (df["numUpvotes"] > 0) |
                          (df["numDownvotes"] > 0) |
                          ((pandas.notna(df["reaction"])) &
                           (df["reaction"] != "invalid")
                           ) |
                          (df["isAssigned"]) |
                          (df["state"] == "closed")
                          ]
        react_series = buildSeriesByCategory(react_df, categories)
        printStatsByCategory(react_df, categories)
        tot_rissues = 0
        for value in react_series:
            tot_rissues += value
        print("Total issues with a reaction: " + str(tot_rissues))
        comments = react_df["numComments"]
        tot_comments = 0
        for value in comments:
            tot_comments += value
        print("Total num. of comments: " + str(tot_comments))

        print("\n#### Ignored issues ####")
        ignored_df = df.loc[(df["fixed (y/n/m)"] == "n") &
                            (df["state"] == "closed") &
                            (df["numUpvotes"] == 0) &
                            (df["numDownvotes"] == 0) &
                            ((pandas.isna(df["reaction"])) |
                             (df["reaction"] == "invalid")
                             )]
        ignored_series = buildSeriesByCategory(ignored_df, categories)
        printStatsByCategory(ignored_df, categories)

        print("\n#### Rejected issues ####")
        # select rows by column values
        rejected_df = df.loc[(df["fixed (y/n/m)"] == "n") &
                             (df["state"] == "closed") &
                             ((df["numDownvotes"] - df["numUpvotes"] > 0) |
                              (df["reaction"] == "negative")  # |
                              # (df["reaction"] == "not-now")
                              )]
        rejected_series = buildSeriesByCategory(rejected_df, categories)
        printStatsByCategory(rejected_df, categories)

        print("\n#### Accepted issues ####")
        accepted_df = df.loc[(df["fixed (y/n/m)"] == "n") &
                             ((df["numDownvotes"] - df["numUpvotes"] < 0) |
                              (df["isAssigned"]) |
                              (df["reaction"] == "positive")
                              )]
        accepted_series = buildSeriesByCategory(accepted_df, categories)
        printStatsByCategory(accepted_df, categories)

        print("\n#### Fixed issues ####")
        # select rows by column values
        fixed_df = df.loc[(df["fixed (y/n/m)"] == "y")]
        fixed_series = buildSeriesByCategory(fixed_df, categories)
        printStatsByCategory(fixed_df, categories)

        print("\n#### Pending issues ####")
        print("the remaining issues that have a pending reaction")

        pending_series = []

        for i in range(4):
            current_tot = 0
            current_tot += ignored_series[i]
            current_tot += rejected_series[i]
            current_tot += accepted_series[i]
            current_tot += fixed_series[i]
            overall_tot = react_series[i]
            pending_series.append(overall_tot - current_tot)


        # Overall results
        print("\n#### Overall stats ####")
        resulting_series = {'ignore': ignored_series, 'reject': rejected_series, 'pending': pending_series,
                            'accept': accepted_series, 'fix': fixed_series, 'reacted': react_series,
                            'opened': openend_series}

        res_df = pandas.DataFrame(resulting_series)
        overall_series = buildOverallResultSeries(resulting_series)
        res_df.loc['overall'] = overall_series

        print(res_df)

        resulting_series_perc = {
            'ignore': res_df['ignore'] / res_df['reacted'] * 100, 'reject': res_df['reject'] / res_df['reacted'] * 100,
            'pending': res_df['pending'] / res_df['reacted'] * 100,
            'accept': res_df['accept'] / res_df['reacted'] * 100,
            'fix': res_df['fix'] / res_df['reacted'] * 100
        }
        print("-> Percentages")
        print(pandas.DataFrame(resulting_series_perc))
        print("-> Reaction rate")
        print(res_df['reacted'] / res_df['opened'] * 100)

        res = convertToRLikertFormat(res_df)
        # print(res)

        # persist in a csv file (for Likert scale in R)
        res.to_csv(path, index=False)

        # Bar chart of most recurrent causes of rejection
        print("\n#### Analysis of rejected issues ####")

        # build the dataframe
        categories_col = []
        comment_labels_col = []
        for index, row in rejected_df.iterrows():
            cat = str(row["category"])
            # fill three label categories
            labels_list = str(row["comment-labels"])
            fillTwoLists("com:", cat, labels_list, categories_col, comment_labels_col)
            bugs_list = str(row["cd-linter-bug"])
            fillTwoLists("bug:", cat, bugs_list, categories_col, comment_labels_col)
            fixes_list = str(row["fix-labels"])
            fillTwoLists("fix:", cat, fixes_list, categories_col, comment_labels_col)

        # print(len(categories_col) == len(comment_labels_col))
        rej_series = {'category': pandas.Series(categories_col),
                      'label': pandas.Series(comment_labels_col)}
        rejc = pandas.DataFrame(rej_series)

        print("-> Overall stats")
        print(" -> Category stats")
        print(rejc['category'].value_counts())
        print(" -> Label stats")
        print(rejc['label'].value_counts())

        rejc_byCat = rejc.groupby('category')
        # print(groupby)

        index = []
        overall_value = []
        for name, group in rejc_byCat:
            print("-> " + name + " : " + str(group.shape[0]))
            ls = group['label']
            print(ls.value_counts())

        print("\n#### Analysis of the resolution time ####")

        res_time = df.loc[(pandas.notna(df["resolution-time"]))]
        res_time = res_time.apply(lambda x: x / (1000 * 60 * 60 * 24) if x.name == 'resolution-time' else x)

        # correlation study
        activity = res_time[["category", "commitsSinceIssue", "contributorsSinceIssue", "resolution-time"]]

        print("---> quick correlation analysis with project activity")
        correlationAnalysis(activity["resolution-time"], activity["commitsSinceIssue"])

        res_time = res_time[["category", "resolution-time"]]
        print("-> Overall")
        print(res_time.describe())
        print("-> Job-Allow-Failure")
        print(res_time.loc[res_time["category"] == "Job-Allow-Failure"].describe())
        print("-> Job-Retry")
        print(res_time.loc[res_time["category"] == "Job-Retry"].describe())
        print("-> Manual-Job")
        print(res_time.loc[res_time["category"] == "Manual-Job"].describe())
        print("-> Versioning")
        print(res_time.loc[res_time["category"] == "Versioning"].describe())


    input_file.close()


def correlationAnalysis(d1, d2):
    covariance = np.cov(d1, d2)
    # print(covariance)

    # Pearson’s Correlation (assume gaussian distribution)
    # calculate Pearson's correlation
    corr, _ = pearsonr(d1, d2)
    print('Pearsons correlation: %.3f' % corr)

    # calculate spearman's correlation (no assumption about the distribution)
    corr, _ = spearmanr(d1, d2)
    print('Spearmans correlation: %.3f' % corr)


if __name__ == '__main__':

    print("RQ1 results")
    rq1cdsmells = "rq1-cdsmells.csv";
    report = 'report.csv' # file that is used as input for generating likert-scaled reactions
    rqone_results(rq1cdsmells, report)

    print("\nRQ2 generate recall sample")
    start_data_file = "analyzedprojects.csv"
    rqtwo_precision = "rq2-precision.csv"
    output_file = "recall-sample.csv"
    categories = {"Job-Allow-Failure", "Job-Retry", "Manual-Job", "Versioning"}
    recallSample(start_data_file, rq1cdsmells, rqtwo_precision, output_file, categories)

    print("\nRQ2 recall results")
    recall_results = "recall-results.csv";
    recall_computation(recall_results)

    print("\nRQ3 results")
    dataset_withyml = "dataset_yml-update.csv"
    rqthree_smells = "rq3-results.csv"
    rqthree_results(rqthree_smells, dataset_withyml)
