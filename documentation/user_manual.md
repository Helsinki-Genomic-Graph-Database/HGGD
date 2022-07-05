# User manual

## Adding data to server

For server access, see [production server access](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/production_server.md#accessing-the-server). This guide assumes running the commands in the `/home/HGGD`-folder where the docker container is running and the `data` and `user_templates` -folders are located.

For a new dataset, add datafiles as a separate folder into the data folder, for example `/data/new_folder`. The `new_folder` should contain the graph and description files in base folder.

If you are adding new files to an existing dataset, add the new files to the dataset folder in question.

When you are adding the files from local computer to the server, you will most likely have to copy the files to a university server (e.g. melkinpaasi.cs.helsinki.fi) first, and from there on to the production server using the `scp`-command. This is because the server can only be accessed directly from the university network. Another option is to download the files from the internet using `wget`-command if the files are somewhere online.

After you add the files or folders, you must [execute the UI](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/user_manual.md#Execution) for the changes to take effect on the website.

The program reads only [.graph (example-file)](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/gt10.kmer15.(128000.130000).V31.E43.cyc72.graph), [.dimacs](https://lcs.ios.ac.cn/~caisw/Resource/about_DIMACS_graph_format.txt) and [.gfa](https://github.com/GFA-spec/GFA-spec/blob/master/GFA-spec.md) -format files (GFA 1.0 support tested, 2.0 should work, but it is not tested as no test data was found) as for the graph files. Other information can be added in description files in .json format.

### Description file

#### Dataset description

The folder can also contain a `description.json` -file that contains information about the dataset. The file can contain [these fields](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/description.json). The required fields are `name` and `descr_short`, others are optional. The UI will still ask whether you want to add the other fields, apart from the `user defined columns` and `sources` that will only be shown if added manually in the file. If the `description.json` -file does not exists upon running the UI, the UI will ask for the missing information for all the necessary fields and create the file. Otherwise it will only ask for information on the missing fields.

The sources in the file will be displayed as www-links, so they should refer to web-pages and start with `https://`. Regular strings will show up as non-working links too.

The licence will appear as a link to the licence definition on the website if the licence is given in SPDX-format. Otherwise the licence will just be a text string on the website. You can find the acceptable SPDX indentifiers [here](https://spdx.org/licenses/), and the UI will notify you if licences are not given in correct SPDX format.

The user defined columns can contain any information the user wants, both in the column name and the information fields. For datasets, this information will appear in a table of its own under the heading `Other information`.

#### Graph description

Each graph can also have a similar `graph_description.json` file. The `graph`-part in the filename should be similar to the graph in question without the file extension. For example `sample.graph` should have a description file called `sample_description.json`. The description file can contain [these fields](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/graph_description.json). The only required field is `descr_short`; others are optional. In this case the UI will not ask for any other information than the short description. It will show the number of graphs in each dataset with no licences and sources in the end, so you can see if something is missing.

The sources will be displayed as www-links here similarly to the dataset descriptions, thus you should provide the source as www-links. You should also provide the licences in SPDX-format if you want them to be shown as links on the website.

The user defined columns can contain any column names and information in graph descriptions same as dataset descriptions. However, they will appear on the dataset page in the `Graphs in the dataset` -table as new columns, so you can compare any information concerning different graphs when they have columns with the same name. All the graphs don't have to contain all the user defined columns. For those lacking certain columns, the table cells will simply be empty. We recommend for graphs not to have more than three different columns so the dataset page table will remain easily readable. On individual graph pages, the information will appear in its own table under the heading `Other information`.

## Execution

After adding the files:

1. Run `sudo docker exec -it hggd bash` to access the docker container.
2. Once you're in the container, run `python3 src/index.py` to execute the console user interface. It checks if the description file exists and if so whether the description file has the all the required information. If necessary, it asks for any missing information. **If this script is not run, then the added data won't be visible on the website.**
3. Exit the container with `exit` command.
4. Restart the container with `sudo docker-compose restart hggd` command.

The user interface **must always be executed** when adding, updating or removing any information or data in the data folder, otherwise the website will not show this dataset.

### New subfolders

The program also makes a `zip`, `sourcetxt` and possibly `dimacs` -folders in the dataset folder.

The `zip`-folder contains all the files in the base folder as a zip-file to download. The download link will appear on the website.

The `sourcetxt`-folder will contain all the source-links as a textfile for the dataset and also for each of the graphs in the `graphs`-subfolder. These are also available as download links on the website.

The `dimacs`-folder will contain the dimacs-files converted from the .graph and .gfa -format files. This folder will not appear if the dataset folder contains only dimacs-format graph files.

There will also be a `log.txt`-file in the dataset folder that will tell when the UI is last executed to compare it to the modification time of the files to see if the files have been added or modified. This is no concern for the user as it is made for the program as a check.

## Removing data

Removing data works from inside the docker container.

1. Run `sudo docker exec -it hggd bash` to access the docker container.
2. Navigate to the data-folder with `cd data` or to the template folder with `cd src/templates/user_templates`. You can remove single files with `rm filename` and folders with `rm -r foldername`. Removing description files without removing the corresponding dataset or graph should not be done.
3. In the case of removing data, the UI should be run afterwards with `python3 src/index.py` in the main directory. If removing templates, both the .json-file and the corresponding html-file in the `pages`-subfolder should be removed.
4. Exit the container with `exit` command.
5. Restart the container with `sudo docker-compose restart hggd` command.

## Updating description files

Description files can be updated by modifying them in the `data` folder. The UI will have to be executed to the changes to take effect:

1. Run `sudo docker exec -it hggd bash` to access the docker container.
2. Once you're in the container, run `python3 src/index.py`.
3. After the UI has been executed exit the container with `exit` command.
4. Restart the container with `sudo docker-compose restart hggd` command.

## Adding user generated html-pages

The sidebar has links to the main page and the Graph Algorithms team page as default. More links can be added to new pages that can be generated from user given .json-files. These files can be added to the `user_templates` folder on the server. The files should contain [these fields](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/html_example.json). The `name`-field should contain the page header and the `content` -file should contain the page body in html-format.

After adding all the page files, the container must be restarted with `sudo docker-compose restart hggd` command. The links will then appear in the sidebar.
