# User manual

## Adding data to server

For server access, see [production server access](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/production_server.md#accessing-the-server).

Add datafiles as a separate folder into the data folder, for example `/data/new_folder`. The `new_folder` should contain the graph files in base folder. The folder can also contain `description.json` that contains the info about the dataset. The file should contain [these fields](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/description.json). The required fields are `name` and `descr_short`, others are optional. The UI will still ask if user wants to add the other fields, apart from the `user defined fields` that will only be shown if added manually to the file. If some graph files are under different licences than the one specified in the description file, a file or several files to contain these exceptions can be added. These files should be labelled as `"licence_name".licence`, and should contain the all graph names (without file extensions) that are under the specific `"licence_name"`-licence, for example [MIT.licence](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/MIT.licence).

After adding the files, run `sudo docker exec -it hggd bash` that allows access to the docker container. There run `python3 src/index.py` that executes the console user interface for the adding of data. It checks either if the description file exist or if the provided description file has the required information. Then it asks for the missing information if needed. If this script is not run, then the added data won't be visible on the website. After this the container can be exited with `exit`. The container must then be restarted with the command `sudo docker-compose restart hggd`.

The user interface **must be executed** always when adding data and also when updating or removing any information in the data folder, otherwise no info of the dataset or the information will not be correct.

The program also makes a `zip` -folder in the `new_folder` with all the files in the base folder as a zip-file to download.
