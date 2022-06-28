import unittest

class TestUiPrintsSummaryOfIssues(unittest.TestCase):
    def setUp(self):
        pass

    def test_if_dataset_nor_graph_have_description_files_and_licence_not_given_in_ui_shows_issues(self):
        pass

    def test_if_dataset_nor_graph_have_description_files_but_spdx_licence_is_given_in_ui_doesnt_show_issues(self):
        pass

    def test_if_dataset_nor_graph_have_description_files_but_non_spdx_licence_is_given_in_ui_shows_issues(self):
        pass

    def test_if_dataset_description_has_spdx_licence_but_graph_doesnt_have_licence_shows_no_issues(self):
        pass

    def test_if_dataset_description_has_spdx_licence_but_graph_has_non_spdx_licence_shows_issues(self):
        pass

    def test_if_all_graphs_have_licence_in_description_but_dataset_doesnt_shows_no_issues(self):
        pass

    def test_if_dataset_has_non_spdx_licence_but_all_graph_have_spdx_licence_shows_no_issues(self):
        pass

    def test_if_dataset_has_non_spdx_licence_but_some_graph_have_spdx_licence_shows_issues(self):
        pass

    def test_if_dataset_and_graphs_have_non_spdx_licences_lists_them_correctly(self):
        pass

    def test_if_graph_doesnt_have_source_shows_issue(self):
        pass

    def test_if_graph_has_source_doesnt_show_issues(self):
        pass

    def test_if_dataset_has_long_desc_in_jsonfile_doesnt_show_issues(self):
        pass

    def test_if_dataset_doesnt_have_long_desc_in_jsonfile_and_not_given_in_ui_shows_issues(self):
        pass

    def test_if_dataset_doesnt_have_long_desc_in_jsonfile_but_its_given_in_ui_doesnt_show_issues(self):
        pass
