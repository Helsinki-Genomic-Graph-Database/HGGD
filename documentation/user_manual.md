# User manual

## Adding data to server

For server access, see [production server access](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/production_server.md#accessing-the-server).

Add datafiles as a separate folder into the data folder, for example `/data/new_folder`. The `new_folder` should contain the graph files in base folder.

### Description file

#### Dataset description

The folder can also contain `description.json` that contains the info about the dataset. The file must contain [these fields](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/description.json). The required fields are `name` and `descr_short`, others are optional. The UI will still ask whether you want to add the other fields, apart from the `user defined fields` and `sources` that will only be shown if added manually to the file. If the `description.json` file does not exists upon running the UI, the UI will ask for all information for all the fields and create the file. Otherwise it will only ask for information on the missing fields. The sources in the file will be displayed as www-links, so they should refer to web-pages and start with `https://`.

#### Graph description

Each graph can also have a similar `graph_description.json` file. The `graph`-part in the filename should be similar to the graph in question without the file extension. For example `sample.graph` should have a description file called `sample_description.json`. The description file should contain [these fields](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/graph_description.json). The only required field is `descr_short`, others are optional. In this case the UI will not ask for any other information than the short description. It will tell how many graphs in each dataset are without licences and sources in the end so missing information can be noticed. The sources will be displayed as www-links here similarly to the dataset descriptions. Similarily to the dataset sources, the sources provided should be www-links.

## Execution

After adding the files:

1. Run `sudo docker exec -it hggd bash` to access the docker container.
2. Once you're in the container, run `python3 src/index.py` to execute the console user interface. It checks if the description file exists and if so whether the description file has the all the required information. If necessary, it asks for the missing information. **If this script is not run, then the added data won't be visible on the website.**
3. Exit the container with `exit` command.
4. Restart the container with `sudo docker-compose restart hggd` command.

The user interface **must always be executed** when adding, updating or removing any information or data in the data folder, otherwise the website will not show this dataset.

### Zip file

The program also makes a `zip` -folder in the `new_folder` with all the files in the base folder as a zip-file to download. The download link will appear on the website.

## Adding user generated html-pages

The sidebar has links to main page and the Graph Algorithms team page as default. More links can be added to new pages that can be generated from user given .json-files. These files can be added to the `user_templates` folder on the server. The files should contain [these fields](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/html_example.json). The `name`-field should contain the page header and the `content` -file should contain the page body in html-format.

After adding all the page files, the container must be restarted with `sudo docker-compose restart hggd` command. Now the links will appear in the sidebar.

## Removing data

Removing data works from inside the docker container.

1. Run `sudo docker exec -it hggd bash` to access the docker container.
2. Navigate to the datafolder with `cd data` or to the template folder with `cd src/templates/user_templates`. You can remove single files with `rm filename` and folders with `rm -r foldername`.
3. In case of removing datafolders, the UI should be run afterwards with `python3 src/index.py` in the main directory. If removing templates, both the .json-file and the corresponding html-file in the `pages`-folder should be removed.
4. Exit the container with `exit` command.
5. Restart the container with `sudo docker-compose restart hggd` command.
