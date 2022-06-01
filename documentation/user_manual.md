# User manual

## Adding data to server

For server access, see [production server access](https://github.com/Helsinki-Genomic-Graph-Database/HGGD/blob/main/documentation/production_server.md#accessing-the-server).

Add datafiles as a separate folder into the data folder, for example `/data/new_folder`. The `new_folder` should contain the graph files in base folder.

After adding the files run `sudo docker exec -it hggd bash` that allows access to the docker container. There run `python3 src/index.py` that runs the console user interface for the adding of data. It checks the description files for the data and ask for the information required if it doesn't exist. If this script is not run, then the added data won't be visible on the website. After this the container can be exited with `exit`. The container must then be restarted with the command `sudo docker-compose restart hggd`.
