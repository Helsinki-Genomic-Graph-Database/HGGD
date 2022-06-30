from datetime import datetime
from src.data_check.json_writer import JsonWriter
from src.data_check.validator import Validator
from src.data_check.zip_creator import ZipCreator
from src.data_check.graph_to_dimacs_converter import GraphToDimacsConverter
from src.data_check.gfa_to_dimacs_converter import GfaToDimacsConverter
from src.file_ui.file_utils import check_file_extension

class UI:
    """This is a text-based user interface for processing
    the dataset so they're ready for the website.
    """
    def __init__(self, dataset_list, input_output, spdx_service):
        self.dataset_list = dataset_list
        self._io = input_output
        self.spdx_service = spdx_service
        self._validator = Validator()
        self._writer = JsonWriter()
        self.something_updated = False
        self.missing_sources = []
        self.missing_licences = []
        self.licences_not_SPDX = set()
        self.issues = {}

    def start(self):
        """This method goes through all the datasets in
        a loop and call the appropriate methods to
        check and add to the data.
        """
        for dataset in self.dataset_list:
            self.something_updated = False
            self._io.write("-------")
            self._io.write("Folder:")
            self._io.write(dataset.get_folder_name())
            self._io.write("Dataset:")

            if dataset.get_name() is None:
                self._io.write("(The dataset has no name)")
            else:
                self._io.write(dataset.get_name())
            if self._validator.check_show_on_website(dataset):
                self._io.write("Folder done.")
                self.process_graph_sources(dataset)
                self.process_graph_licences(dataset)
                self.process_issues(dataset)
                continue
            data_exists = self.process_data(dataset)
            if not data_exists:
                continue
            json_path = self._writer.get_json_path(dataset)
            questions_asked = self.process_json_file(dataset, json_path)
            self.something_updated = questions_asked
            self.process_name(dataset)
            self.process_short_desc(dataset)
            self.process_long_description(dataset, questions_asked)
            self.process_licence(dataset, questions_asked)
            self.process_graph_description(dataset)
            self.process_graph_sources(dataset)
            self.process_graph_licences(dataset)
            self.process_issues(dataset)
            self.create_dimacs(dataset)
            self.folder_done(dataset)

        self.print_number_of_issues()

    def print_number_of_issues(self):
        number_of_issues = len(self.issues) + len(self.missing_licences) + len(self.missing_sources)
        if number_of_issues > 0:
            self._io.write(f"\033[1;33;40m{number_of_issues} issue(s) found in datasets\033[0;37;40m")
            self._io.write("\033[1;33;40mShow issues in detail? (y/n)\033[0;37;40m")
            command = self._io.read("")
            if command.lower() != "n":
                self.print_issues()

    def print_issues(self):
        for folder in self.issues:
            name, issues = self.issues[folder]

            for issue in issues:
                self._io.write(f"\033[1;33;40mDataset '{name}' in folder '{folder}' {issue}.\033[0;37;40m")

        self.print_missing_sources()
        self.print_missing_licences()
        self.print_non_spdx_licences()

    def process_issues(self, dataset):
        issues = []
        if not self._validator.check_data_exists(dataset):
            issues.append("has no data")

        if not self._validator.check_descr_long_exists(dataset):
            issues.append("has no long description")

        if dataset.get_licence():
            for licence in dataset.get_licence():
                if not licence is None:
                    spdx_issue = "has a licence that is not in SPDX format"
                    if not self._validator.check_if_licence_in_spdx_format(licence):
                        if not spdx_issue in issues:
                            issues.append(spdx_issue)

        if len(issues) > 0:
            self.issues[dataset.get_folder_name()] = (dataset.get_name(), issues)

    def process_graph_sources(self, dataset):
        number_of_missing_sources = self._validator.count_graphs_without_sources(dataset)
        if number_of_missing_sources > 0:
            self.missing_sources.append((dataset.get_name(), dataset.get_folder_name(), \
                number_of_missing_sources))

    def print_missing_sources(self):
        if len(self.missing_sources) > 0:
            for dataset in self.missing_sources:
                self._io.write(f"\033[1;33;40mDataset '{dataset[0]}' in folder '{dataset[1]}' has \
{dataset[2]} graph(s) with missing source files.\033[0;37;40m")

    def print_non_spdx_licences(self):
        if len(self.licences_not_SPDX) > 0:
            self._io.write("These licences are not in SPDX format: ")
            for licence in self.licences_not_SPDX:
                if not licence is None:
                    self._io.write(licence)

    def process_graph_description(self, dataset):
        graph_list = dataset.get_list_of_graphs()
        for graph in graph_list:
            if not self._validator.check_graph_short_description(graph):
                short_desc = self.ask_sh_desc_graph(graph.get_file_name())
                if self._validator.check_graph_description_file_exists(graph):
                    self._writer.update_graph_description(dataset, graph.get_file_name(), short_desc)
                    self._io.write("\033[1;32;40mGraph description-file updated.\033[0;37;40m")
                else:
                    self._writer.create_graph_description(dataset, graph.get_file_name(), short_desc)
                    self._io.write("\033[1;32;40mGraph description-file created.\033[0;37;40m")
        self._io.write("\033[1;32;40mAll graphs in dataset have a description.\033[0;37;40m")

    def process_graph_licences(self, dataset):
        number_of_missing_licences = self._validator.count_graphs_without_licence(dataset)
        if number_of_missing_licences > 0 and not self._validator.check_licence_exists(dataset):
            self.missing_licences.append((dataset.get_name(), dataset.get_folder_name(), \
                number_of_missing_licences))
        for graph in dataset.get_list_of_graphs():
            graph_licence = graph.get_licence()
            if not graph_licence is None:
                spdx_format = self._validator.check_if_licence_in_spdx_format(graph_licence)
                if spdx_format is False:
                    self.licences_not_SPDX.update(graph_licence)

    def print_missing_licences(self):
        if len(self.missing_licences) > 0:
            for dataset in self.missing_licences:
                self._io.write(f"\033[1;33;40mDataset '{dataset[0]}' in folder '{dataset[1]}' has \
{dataset[2]} graph(s) with no licence given.\033[0;37;40m")

    def process_data(self, dataset):
        data_exists = self._validator.check_data_exists(dataset)
        if not data_exists:
            print_out = "\033[1;33;40mThere is no data in \
folder "+dataset.get_folder_name()+".\033[0;37;40m"
            self._io.write(print_out)
            self._io.write("Folder done.")
            return False
        self._io.write("\033[1;32;40mData exists.\033[0;37;40m")
        return True

    def process_json_file(self, dataset, json_path):
        questions_asked = False
        json_exists = self._validator.check_dataset_description_file_exists(dataset)
        if json_exists:
            json_empty = self._validator.check_description_file_empty(json_path)
        if not json_exists or json_empty:
            name = self.ask_name()
            sh_desc = self.ask_sh_desc()
            long_desc = self.ask_long_desc()
            licence = self.ask_for_licence()
            if len(licence) == 0:
                licence = None
            if not licence is None:
                licence = self.spdx_service.create_licence_link_tuples(licence)
                self._writer.create_json_file(dataset, name, sh_desc, long_desc, licence[0])
                self.something_updated = True
                self.process_licence_format(licence)
                dataset.update_licence(licence)
            else:
                self._writer.create_json_file(dataset, name, sh_desc, long_desc, licence)
                self.something_updated = True
            dataset.set_name(name)
            dataset.set_descr_short(sh_desc)
            dataset.set_descr_long(long_desc)
            dataset.set_description_file_exists(True)
            questions_asked = True
        self._io.write("\033[1;32;40mJson-file exists.\033[0;37;40m")
        return questions_asked

    def process_name(self, dataset):
        name_exists = self._validator.check_name_exists(dataset)
        if not name_exists:
            name = self.ask_name()
            dataset.set_name(name)
            self._writer.update_json_file(dataset, "name", name)
            self.something_updated = True
        self._io.write("\033[1;32;40mName exists.\033[0;37;40m")

    def process_short_desc(self, dataset):
        short_desc_exists = self._validator.check_dataset_descr_short_exists(dataset)
        if not short_desc_exists:
            sh_desc = self.ask_sh_desc()
            dataset.set_descr_short(sh_desc)
            self._writer.update_json_file(dataset, "descr_short", sh_desc)
            self.something_updated = True
        self._io.write("\033[1;32;40mShort description exists.\033[0;37;40m")

    def process_long_description(self, dataset, questions_asked):
        long_desc_exists = self._validator.check_descr_long_exists(dataset)
        long_desc = dataset.get_descr_long()
        if not questions_asked:
            if not long_desc_exists:
                long_desc = self.ask_long_desc()
                dataset.set_descr_long(long_desc)
                self._writer.update_json_file(dataset, "descr_long", long_desc)
                self.something_updated = True
        if long_desc == "":
            self._io.write("\033[1;33;40mYou chose that the dataset \
doesn't have a long description.\033[0;37;40m")
        else:
            self._io.write("\033[1;32;40mLong description exists.\033[0;37;40m")

    def process_licence(self, dataset, questions_asked):
        licence_exists = self._validator.check_licence_exists(dataset)
        licence = dataset.get_licence()
        if not questions_asked:
            if not licence_exists:
                licence = self.ask_for_licence()
                if licence == "":
                    licence = None
                if not licence is None:
                    self._writer.update_json_file(dataset, "licence", licence)
                    licence = self.spdx_service.create_licence_link_tuples(licence)
                    self.something_updated = True
                    self.process_licence_format(licence)
                    dataset.update_licence(licence)
        if licence is None or len(licence) == 0:
            self._io.write("\033[1;33;40mYou chose that the dataset \
doesn't have a licence.\033[0;37;40m")
        else:
            self._io.write("\033[1;32;40mLicence exists.\033[0;37;40m")

    def process_licence_format(self, licence):
        spdx_format = self._validator.check_if_licence_in_spdx_format(licence)
        if spdx_format is False:
            self.licences_not_SPDX.update(licence)
            self._io.write("\033[1;33;40mThe licence you gave is not in SPDX format, \
so a link to the SPDX website will NOT be generated.\033[0;37;40m If you want to give the licence \
in SPDX format, please edit the description file and run UI again.")

    def ask_name(self):
        name = ""
        while name == "":
            self._io.write("\033[1;31;40mThe dataset has no name.\033[0;37;40m")
            name = self._io.read("Please give a name: ")
        return name

    def ask_sh_desc(self):
        sh_desc = ""
        while sh_desc == "":
            self._io.write("\033[1;31;40mThe dataset doesn't \
have a short description.\033[0;37;40m")
            sh_desc = self._io.read("Please give a short description: ")
        return sh_desc

    def ask_long_desc(self):
        self._io.write("\033[1;31;40mThe dataset doesn't have a long description.\033[0;37;40m")
        long_desc = self._io.read("Please give a long description or leave empty: ")
        return long_desc

    def ask_for_licence(self):
        self._io.write("\033[1;31;40mThe dataset has no licence.\033[0;37;40m")
        licence = self._io.read("Which licence is the dataset under? (Leave empty if no licence.) ")
        return licence

    def ask_sh_desc_graph(self, graph):
        sh_desc = ""
        while sh_desc == "":
            self._io.write(f"\033[1;31;40mThe graph file '{str(graph)}' doesn't \
have a short description.\033[0;37;40m")
            sh_desc = self._io.read("Please give a short description: ")
        return sh_desc

    def folder_done(self, dataset):
        """
        This method creates a log.txt file to save the date
        and time when the ui was last run and a zip-file for the
        dataset's graphs for the website.

        Args:
            dataset
        """
        if dataset.get_has_log_file() or self.something_updated:
            self._io.write("Data has been checked and updated.")
        else:
            self._io.write("Data has been checked.")
        self._io.write("Folder done.")
        path = dataset.get_path()
        name = dataset.get_folder_name()
        logstamp = datetime.now().isoformat(" ", "seconds")
        with open(path+"/log.txt", "w", encoding='utf-8') as log:
            log.write(f"ui run on: {logstamp}")
        zip_c = ZipCreator()
        zip_c.create_zip(name, path)

    def create_dimacs(self, dataset):
        graph_list = dataset.get_list_of_graphs()
        dimacs_converter = GraphToDimacsConverter(dataset.get_path())
        gfa_to_dimacs_converter = GfaToDimacsConverter(dataset.get_path())
        for graph in graph_list:
            if check_file_extension(graph.get_file_name(), "graph"):
                dimacs_converter.convert_graph_to_dimacs(graph.get_file_name())
            elif check_file_extension(graph.get_file_name(), "gfa"):
                gfa_to_dimacs_converter.convert_gfa_to_dimacs(graph.get_file_name())
